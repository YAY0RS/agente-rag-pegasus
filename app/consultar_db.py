import os
from operator import itemgetter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Estructuras de datos con memoria
class Mensaje(BaseModel):
    rol: str
    contenido: str

class PreguntaRequest(BaseModel):
    pregunta: str
    historial: List[Mensaje] = []  # Recibe el historial como una lista vacía por defecto

# 2. Inicializamos FastAPI
app = FastAPI(title="API Agente RAG - Santo Pegasus Soluciones")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agente_rag = None
buscador_global = None

# 3. Configuramos el agente
@app.on_event("startup")
def cargar_agente():
    global agente_rag, buscador_global
    print("Cargando base de datos vectorial y modelos de IA...")
    
    modelo_embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    directorio_db = "./data/chroma_db"
    vector_db = Chroma(persist_directory=directorio_db, embedding_function=modelo_embeddings)
    
    retriever = vector_db.as_retriever(search_kwargs={"k": 8})
    buscador_global = retriever
    
    llm = ChatCohere(model="command-r-08-2024", temperature=0.3)
    
    # NUEVO PROMPT: Le agregamos la variable {historial}
    system_prompt = (
        "Eres un asistente virtual experto en la documentación técnica de Santo Pegasus Soluciones.\n"
        "Tu objetivo es responder a las preguntas de los desarrolladores de forma clara, profesional y concisa.\n"
        "Utiliza estrictamente el contexto de los manuales y el historial de la conversación para responder.\n"
        "Si la respuesta no se encuentra en el contexto, di amablemente: 'Lo siento, esa información no está "
        "disponible en la documentación actual.' No inventes datos.\n\n"
        "Historial de la conversación previa:\n{historial}\n\n"
        "Contexto de los manuales:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # NUEVA CADENA LCEL: Mapeamos las variables de entrada
    agente_rag = (
        {
            "context": itemgetter("pregunta") | retriever | format_docs, 
            "input": itemgetter("pregunta"),
            "historial": itemgetter("historial")
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    print("¡Agente RAG listo para recibir peticiones!")

# 4. Endpoint principal
@app.post("/preguntar")
async def consultar_agente(request: PreguntaRequest):
    if not agente_rag or not buscador_global:
        raise HTTPException(status_code=500, detail="El agente no está inicializado.")
    
    try:
        # Formateamos el historial para que la IA lo entienda como texto
        texto_historial = "\n".join([f"{m.rol}: {m.contenido}" for m in request.historial])
        if not texto_historial:
            texto_historial = "No hay conversación previa."

        # Invocamos al agente pasándole ambas cosas
        respuesta = agente_rag.invoke({
            "pregunta": request.pregunta,
            "historial": texto_historial
        })
        
        return {"pregunta": request.pregunta, "respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
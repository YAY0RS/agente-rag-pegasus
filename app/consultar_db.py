import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Definimos la estructura de datos
class PreguntaRequest(BaseModel):
    pregunta: str

# 2. Inicializamos FastAPI
app = FastAPI(title="API Agente RAG - Santo Pegasus Soluciones")

# --- NUEVO: Configuración de CORS ---
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que cualquier página web se conecte (ideal para desarrollo local)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales seguras
agente_rag = None
buscador_global = None  # <--- Añadimos esta variable para el Rayo X

# 3. Configuramos el agente
@app.on_event("startup")
def cargar_agente():
    global agente_rag, buscador_global
    print("Cargando base de datos vectorial y modelos de IA...")
    
    modelo_embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    directorio_db = "./data/chroma_db"
    vector_db = Chroma(persist_directory=directorio_db, embedding_function=modelo_embeddings)
    
    # Aumentamos a 8 fragmentos para mayor contexto
    retriever = vector_db.as_retriever(search_kwargs={"k": 8})
    buscador_global = retriever  # <--- Guardamos la referencia limpia aquí
    
    llm = ChatCohere(model="command-r-08-2024", temperature=0.3)
    
    system_prompt = (
        "Eres un asistente virtual experto en la documentación técnica de Santo Pegasus Soluciones.\n"
        "Tu objetivo es responder a las preguntas de los desarrolladores de forma clara, profesional y concisa, "
        "utilizando estrictamente el contexto proporcionado abajo.\n"
        "Si la respuesta no se encuentra en el contexto, di amablemente: 'Lo siento, esa información no está "
        "disponible en la documentación actual.' No inventes datos.\n\n"
        "Contexto de los manuales:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    agente_rag = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("¡Agente RAG listo para recibir peticiones!")

# 4. Creamos el endpoint principal
@app.post("/preguntar")
async def consultar_agente(request: PreguntaRequest):
    if not agente_rag or not buscador_global:
        raise HTTPException(status_code=500, detail="El agente no está inicializado.")
    
    try:
        # --- 🔍 RAYO X SEGURO ---
        # Consultamos directamente a la variable global sin romper LangChain
        docs_recuperados = buscador_global.invoke(request.pregunta)
        
        print(f"\n--- 🔍 RAYO X: LEYENDO {len(docs_recuperados)} FRAGMENTOS ---")
        for i, doc in enumerate(docs_recuperados):
            print(f"\n[Fragmento {i+1}]: {doc.page_content}")
        print("----------------------------------------------------------\n")
        # ------------------------

        # Invocamos al agente
        respuesta = agente_rag.invoke(request.pregunta)
        return {"pregunta": request.pregunta, "respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
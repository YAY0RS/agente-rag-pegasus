import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Cargar variables de entorno
load_dotenv()

def procesar_directorio():
    ruta_docs = "./data/documentos"
    directorio_db = "./data/chroma_db"

    # 1. Encontrar todos los archivos PDF en la carpeta
    archivos_pdf = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
    
    if not archivos_pdf:
        print("No se encontraron PDFs en la carpeta.")
        return

    documentos_totales = []
    print(f"Se encontraron {len(archivos_pdf)} documentos. Iniciando procesamiento...\n")
    
    # 2. Cargar cada PDF
    for archivo in archivos_pdf:
        ruta_completa = os.path.join(ruta_docs, archivo)
        print(f"-> Leyendo: {archivo}")
        loader = PyPDFLoader(ruta_completa)
        documentos_totales.extend(loader.load())

    print(f"\nSe extrajeron {len(documentos_totales)} páginas en total.")

    # 3. Dividir el texto de toda la biblioteca
    print("Dividiendo los documentos en fragmentos semánticos...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    fragmentos = text_splitter.split_documents(documentos_totales)

    # 4. Generar embeddings y guardar en Chroma DB
    print("Generando vectores matemáticos y guardando en Chroma DB (esto puede tomar un momento)...")
    modelo_embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    Chroma.from_documents(
        documents=fragmentos,
        embedding=modelo_embeddings,
        persist_directory=directorio_db
    )
    print("\n¡Éxito! La base de datos vectorial ha sido actualizada con todos los manuales.")

if __name__ == "__main__":
    procesar_directorio()
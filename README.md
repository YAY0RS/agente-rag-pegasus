# 🚀 Agente RAG Corporativo - Santo Pegasus Soluciones

Un sistema completo de Inteligencia Artificial utilizando la arquitectura **Retrieval-Augmented Generation (RAG)** para interactuar con la documentación técnica y manuales de ingeniería de la empresa.

Este proyecto fue desarrollado como parte de las implementaciones prácticas de la etapa **Tech Builder** del programa **Oracle Next Education (ONE)**.

## 🧠 Arquitectura y Tecnologías

El proyecto sigue una arquitectura Full-Stack contenerizada, dividida en un motor de Inteligencia Artificial (Back-end) y una interfaz de usuario (Front-end).

- **Inteligencia Artificial y NLP:** LangChain, Cohere (`command-r-08-2024`), HuggingFace Embeddings.
- **Base de Datos Vectorial:** ChromaDB (Almacenamiento semántico local).
- **Back-end:** FastAPI (Python), Uvicorn.
- **Front-end:** HTML5, CSS3, Vanilla JavaScript (Fetch API).
- **Infraestructura y DevOps:** Docker, Docker Compose.

## ✨ Características Principales (MVP)

- **Búsqueda Semántica:** Ingesta y segmentación de múltiples documentos PDF técnicos (Arquitectura, Bases de Datos, Procesos).
- **Cero Alucinaciones:** El agente está restringido por un `System Prompt` estricto que le impide inventar información fuera de la documentación oficial.
- **Memoria de Contexto:** El cliente web gestiona el historial de la conversación, permitiendo al usuario hacer preguntas de seguimiento de forma natural.
- **UI/UX Profesional:** Interfaz gráfica responsiva tipo terminal corporativa, con un área de texto auto-ajustable (`auto-resize`) y soporte para saltos de línea combinados (`Shift + Enter`).

## 🛠️ Requisitos Previos

Para ejecutar este proyecto en tu entorno local necesitas:

- [Docker](https://www.docker.com/) y Docker Compose instalados.
- Una API Key válida de [Cohere](https://cohere.com/).

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/YAYORS/agente-rag-pegasus.git](https://github.com/YAYORS/agente-rag-pegasus.git)
   cd agente-rag-pegasus
   ```

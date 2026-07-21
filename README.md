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

## 💬 Ejemplos de Uso

Aquí tienes algunas preguntas que el agente puede responder basándose en los manuales de Santo Pegasus:

**Usuario:** *"¿Qué base de datos utiliza el servicio de usuarios?"*
**Agente RAG:** *"El servicio de usuarios (`user-service`) utiliza una base de datos PostgreSQL 15 RDS Multi-AZ denominada `users_db`. Esta base de datos es utilizada para almacenar datos relacionales de perfil de los usuarios."*

**Usuario:** *"Si ocurre un incidente grave en producción, ¿cuáles son los pasos a seguir?"*
**Agente RAG:** *"Según el manual de incidentes, en caso de que se caiga el servidor de producción, debes notificar al Incident Commander de turno y al líder técnico del servicio afectado..."*

**Usuario:** *"¿Cuáles son los pasos para configurar mi entorno local de front-end?"*
**Agente RAG:** *"Para configurar tu entorno local... 1. Asegúrate de tener instalado NVM... 2. Instala VS Code... 3. Ejecuta `npm install`..."*

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
2. **Variables de Entorno**
   Crea un archivo .env en la raíz del proyecto y agrega tu llave de Cohere:
   ```
   COHERE_API_KEY=tu_api_key_aqui
   ```
3. **Cargar los documentos fuente**
   Como los manuales no se suben a GitHub por privacidad, debes crear la carpeta de datos y colocar tus PDFs técnicos allí:
   Crea la ruta: data/documentos/
   Pega dentro de esa carpeta todos los archivos .pdf que la IA deberá leer.

4. **Levantar la infraestructura con Docker**
   en la terminal situado en la raiz del proyecto (a la altura del docker) poner el sieguiente comando
   ```
   docker-compose up -d --build
   ```
5. **Crear la Base de Datos Vectorial (Ingesta de datos)**
   Antes de hacer preguntas, debes procesar los PDFs para que LangChain los fragmente y los guarde matemáticamente en ChromaDB. Ejecuta este comando en tu terminal para correr el script dentro del contenedor:
   ```
   docker-compose exec agente_rag python procesar_documento.py
   ```
   (Espera a que la consola indique que los fragmentos se han guardado exitosamente).
   **6. Acceso a los servicios:**

- **Front-end (Chat UI):** Abre el archivo `frontend/index.html` directamente en tu navegador web.
- **API de FastAPI (Swagger UI):** Navega a `http://localhost:8000/docs`.

## 🗺️ Roadmap y Próximas Mejoras

- [ ] **Advanced RAG (History-Aware Retriever):** Implementar una reformulación de búsqueda con LangChain para evitar la dilución semántica al cambiar de contexto en conversaciones largas.
- [ ] **Despliegue en la Nube:** Migrar el contenedor de Docker a una instancia de Oracle Cloud Infrastructure (OCI).

---

_Desarrollado por Eduardo García Morales._

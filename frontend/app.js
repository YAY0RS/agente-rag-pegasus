const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Función para agregar mensajes al DOM
function addMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message");
  msgDiv.classList.add(sender === "user" ? "user-message" : "system-message");
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  // Hacer scroll automático hacia abajo
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Lógica principal de comunicación con la API RAG
async function askAgent() {
  const text = userInput.value.trim();
  if (!text) return;

  // 1. Pintar mensaje del usuario
  addMessage(text, "user");
  userInput.value = "";

  // Bloquear input mientras carga
  userInput.disabled = true;
  sendBtn.disabled = true;
  sendBtn.textContent = "...";

  try {
    // 2. Hacer petición al contenedor de Docker (FastAPI)
    const response = await fetch("http://localhost:8000/preguntar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ pregunta: text }),
    });

    if (!response.ok) {
      throw new Error("Error en el servidor");
    }

    const data = await response.json();

    // 3. Pintar la respuesta de la IA
    addMessage(data.respuesta, "system");
  } catch (error) {
    addMessage(
      "Hubo un error de conexión con el agente. Verifica que el servidor de Docker esté encendido.",
      "system",
    );
    console.error(error);
  } finally {
    // Desbloquear input
    userInput.disabled = false;
    sendBtn.disabled = false;
    sendBtn.textContent = "Enviar";
    userInput.focus();
  }
}

// Eventos de click y tecla Enter
sendBtn.addEventListener("click", askAgent);

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    askAgent();
  }
});

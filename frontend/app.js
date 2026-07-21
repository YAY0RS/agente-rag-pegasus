const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// --- NUEVA MEMORIA DEL NAVEGADOR ---
let historialChat = [];
// -----------------------------------

function addMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message");
  msgDiv.classList.add(sender === "user" ? "user-message" : "system-message");
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function askAgent() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";
  userInput.style.height = "auto"; // <--- AGREGA ESTA LÍNEA AQUÍ

  userInput.disabled = true;
  sendBtn.disabled = true;
  sendBtn.textContent = "...";

  try {
    const response = await fetch("http://localhost:8000/preguntar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // NUEVO: Enviamos la pregunta + la memoria acumulada
      body: JSON.stringify({
        pregunta: text,
        historial: historialChat,
      }),
    });

    if (!response.ok) {
      throw new Error("Error en el servidor");
    }

    const data = await response.json();
    addMessage(data.respuesta, "system");

    // NUEVO: Guardamos la plática actual en la memoria para la siguiente pregunta
    historialChat.push({ rol: "Usuario", contenido: text });
    historialChat.push({ rol: "Asistente", contenido: data.respuesta });
  } catch (error) {
    addMessage(
      "Hubo un error de conexión con el agente. Verifica el servidor.",
      "system",
    );
    console.error(error);
  } finally {
    userInput.disabled = false;
    sendBtn.disabled = false;
    sendBtn.textContent = "Enviar";
    userInput.focus();
  }
}
// ==========================================
// EVENTOS DE LA CAJA DE TEXTO Y BOTÓN
// ==========================================

// 1. Auto-expandir la caja mientras escribes
userInput.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";

  if (this.scrollHeight > 200) {
    this.style.overflowY = "auto";
  } else {
    this.style.overflowY = "hidden";
  }
});

// 2. Manejar la tecla Enter y Shift + Enter
userInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    if (!e.shiftKey) {
      e.preventDefault(); // Evita que se haga un salto de línea
      askAgent(); // Envía el mensaje al backend
    }
    // Si estás presionando Shift, simplemente ignora el preventDefault
    // y deja que el textarea haga su salto de línea natural.
  }
});

// 3. Enviar al hacer clic en el botón azul
sendBtn.addEventListener("click", askAgent);

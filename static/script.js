const messagesContainer = document.getElementById("messages");
const userInput = document.getElementById("userInput");

function createMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.textContent = text;
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingAnimation() {
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "bot");
  typingDiv.innerHTML =
    '<span class="typing"></span><span class="typing"></span><span class="typing"></span>';
  messagesContainer.appendChild(typingDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  return typingDiv;
}

async function sendMessage() {
  const question = userInput.value.trim();
  if (!question) return;

  createMessage(question, "user");
  userInput.value = "";

  const typingDiv = showTypingAnimation();

  try {
    const response = await fetch("/get-answer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();
    setTimeout(() => {
      typingDiv.remove();
      const answer = data.answer || "Unable to answer.";
      createMessage(answer, "bot");
    }, 2000);
  } catch (error) {
    setTimeout(() => {
      typingDiv.remove();
      createMessage("Unable to answer.", "bot");
    }, 2000);
  }
}

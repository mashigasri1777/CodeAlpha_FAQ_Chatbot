async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const question = input.value.trim();

  if (!question) return;

  chatBox.innerHTML += `<div class="user-msg">${question}</div>`;
  input.value = "";

  const response = await fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  });

  const data = await response.json();
  chatBox.innerHTML += `<div class="bot-msg">${data.answer}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}

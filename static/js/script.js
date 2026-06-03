async function sendMessage() {

    const input =
        document.getElementById("user-input");

    const chatBox =
        document.getElementById("chat-box");

    const question =
        input.value.trim();

    if (!question) return;

    chatBox.innerHTML += `
        <div class="user-message">
            ${question}
        </div>
    `;

    input.value = "";

    try {

        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            });

        const data =
            await response.json();

        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.answer}
            </div>
        `;

        chatBox.scrollTop =
            chatBox.scrollHeight;

    }

    catch (error) {

        chatBox.innerHTML += `
            <div class="bot-message">
                Server error. Please try again.
            </div>
        `;
    }
}

document
.getElementById("user-input")
.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();
    }
});

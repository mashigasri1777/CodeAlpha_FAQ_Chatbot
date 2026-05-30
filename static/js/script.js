async function sendMessage() {

```
const input =
    document.getElementById("user-input");

const chatBox =
    document.getElementById("chat-box");

const question =
    input.value.trim();

if (!question) return;

// User Message

chatBox.innerHTML += `
    <div class="user-message">
        ${question}
    </div>
`;

input.value = "";

chatBox.scrollTop =
    chatBox.scrollHeight;

// Typing Indicator

const typingId =
    "typing-" + Date.now();

chatBox.innerHTML += `
    <div class="bot-message"
         id="${typingId}">
        Typing...
    </div>
`;

chatBox.scrollTop =
    chatBox.scrollHeight;

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

    // Small delay for chatbot feel

    await new Promise(resolve =>
        setTimeout(resolve, 800)
    );

    document
        .getElementById(typingId)
        .remove();

    let confidenceText = "";

    if (data.confidence) {

        confidenceText =
            `<br><small>
            Confidence:
            ${data.confidence}%
            </small>`;
    }

    chatBox.innerHTML += `
        <div class="bot-message">
            ${data.answer}
            ${confidenceText}
        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;

}

catch (error) {

    document
        .getElementById(typingId)
        .remove();

    chatBox.innerHTML += `
        <div class="bot-message">
            Sorry, something went wrong.
        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}
```

}

// Enter key support

document
.getElementById("user-input")
.addEventListener("keypress",
function(event){

```
if(event.key === "Enter"){

    sendMessage();
}
```

});

// Auto focus input

window.onload = function(){

```
document
.getElementById("user-input")
.focus();
```

};

function handleKeyPress(event) {
    if (event.key === "Enter") { sendMessage(); }
}

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    if (message === "") return;

    const chatBox = document.getElementById("chat-box");
    
    chatBox.innerHTML += `<div class="message user-message">${message}</div>`;
    inputField.value = "";
    
    const loadingId = "loading-" + Date.now();
    chatBox.innerHTML += `<div id="${loadingId}" class="message bot-message"><i>Typing...</i></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div class="message bot-message">${data.reply}</div>`;
    } catch (error) {
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div class="message bot-message" style="color:red;">Internet ya Server me problem hai!</div>`;
    }
    
    chatBox.scrollTop = chatBox.scrollHeight;
}
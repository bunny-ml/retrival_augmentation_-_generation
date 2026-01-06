const API_URL = "http://127.0.0.1:5000";

function handleKeyPress(e) {
    if (e.key === 'Enter') sendMessage();
}

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const userId = document.getElementById('userId').value;
    const status = document.getElementById('uploadStatus');
    const btn = document.getElementById('uploadBtn');

    if (!fileInput.files[0]) return alert("Select a file first!");
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("user_id", userId);

    // UI State: Loading
    btn.disabled = true;
    status.innerText = "⏳ Indexing document...";

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });
        const result = await response.json();
        status.innerText = result.message || result.error;
    } catch (err) {
        status.innerText = "❌ Connection failed";
    } finally {
        btn.disabled = false;
    }
}

async function sendMessage() {
    const input = document.getElementById('userMessage');
    const chatWindow = document.getElementById('chatWindow');
    const userId = document.getElementById('userId').value;
    const msg = input.value.trim();

    if (!msg) return;

    
    appendMsg("user-msg", msg);
    input.value = "";

    
    const loaderId = "loader-" + Date.now();
    appendMsg("bot-msg", "Thinking...", loaderId);

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, message: msg })
        });
        const result = await response.json();
        
        
        document.getElementById(loaderId).innerText = result.response || result.error;
    } catch (err) {
        document.getElementById(loaderId).innerText = "❌ Error: Could not reach backend.";
    }
}

function appendMsg(type, text, id = null) {
    const win = document.getElementById('chatWindow');
    const div = document.createElement('div');
    div.className = `msg ${type}`;
    if (id) div.id = id;
    div.innerText = text;
    win.appendChild(div);
    win.scrollTop = win.scrollHeight;
}
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const micBtn = document.getElementById("mic-btn");
const attachBtn = document.getElementById("attach-btn");

const sessionId = "user1";

// Chat message function
function addMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("chat-message", role);
    msgDiv.innerText = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send text message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    addMessage("user", message);
    userInput.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat/text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, message })
        });
        const data = await response.json();
        addMessage("bot", data.reply);
    } catch (err) {
        addMessage("bot", "Error connecting to backend.");
        console.error(err);
    }
}

// Enter key
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
sendBtn.addEventListener("click", sendMessage);

// Voice input
micBtn.addEventListener("click", async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Microphone not supported.");
        return;
    }

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", audioBlob);
            formData.append("session_id", sessionId);

            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/chat/voice?session_id=${sessionId}`,
                    { method: "POST", body: formData }
                );
                const data = await response.json();
                addMessage("user", data.transcription);
                addMessage("bot", data.reply);
            } catch (err) {
                addMessage("bot", "Error connecting to backend.");
                console.error(err);
            }
        };

        mediaRecorder.start();
        setTimeout(() => {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
        }, 5000);

    } catch (err) {
        console.error(err);
        alert("Error accessing microphone: " + err);
    }
});

// Attach button
attachBtn.addEventListener("click", () => {
    alert("Attach file functionality coming soon!");
});

// ---------------------
// Live EST Clock
// ---------------------
function updateClock() {
    const options = {
        timeZone: 'America/New_York',
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    };
    const now = new Date();
    const formatter = new Intl.DateTimeFormat([], options);
    document.getElementById('live-clock').textContent = formatter.format(now);
}

// Update every second
setInterval(updateClock, 1000);
updateClock(); // initial call

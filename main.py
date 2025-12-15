# app/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.memory import get_history, save_message
from app.llm import generate_response
from fastapi.middleware.cors import CORSMiddleware
from app.stt import transcribe_audio  # We’ll create this next

app = FastAPI(title="Utility AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for text chat
class ChatRequest(BaseModel):
    session_id: str
    message: str

# Text chat endpoint
@app.post("/chat/text")
async def chat_text(req: ChatRequest):
    # Save user message
    save_message(req.session_id, "user", req.message)
    
    # Get full session history
    history = get_history(req.session_id)
    
    # Get chatbot reply
    reply = await generate_response(history)
    
    # Save assistant reply
    save_message(req.session_id, "assistant", reply)
    
    return {"reply": reply}

# Voice chat endpoint
@app.post("/chat/voice")
async def chat_voice(session_id: str, audio: UploadFile = File(...)):
    # Read audio bytes
    audio_bytes = await audio.read()
    
    # Convert speech to text
    text = transcribe_audio(audio_bytes)
    
    # Save user message
    save_message(session_id, "user", text)
    
    # Get session history
    history = get_history(session_id)
    
    # Get chatbot reply
    reply = await generate_response(history)
    
    # Save assistant reply
    save_message(session_id, "assistant", reply)
    
    return {"transcription": text, "reply": reply}

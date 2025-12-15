# app/stt.py
import whisper
import tempfile

# Load the model once globally for efficiency
model = whisper.load_model("base")  # You can use "small" or "medium" if needed

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Converts audio bytes to text using Whisper.
    """
    # Save bytes to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file.flush()
        # Transcribe using Whisper
        result = model.transcribe(tmp_file.name)
        return result["text"]
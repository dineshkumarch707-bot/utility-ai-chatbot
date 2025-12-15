# app/memory.py

# In-memory dictionary to store conversations per session
conversation_store = {}

def get_history(session_id: str):
    """
    Retrieve conversation history for a given session_id.
    Returns a list of messages in the format:
    [{"role": "user", "content": "..."},
     {"role": "assistant", "content": "..."}]
    """
    return conversation_store.get(session_id, [])

def save_message(session_id: str, role: str, content: str):
    """
    Save a message to the conversation store.
    role: 'user' or 'assistant'
    content: message text
    """
    conversation_store.setdefault(session_id, []).append(
        {"role": role, "content": content}
    )
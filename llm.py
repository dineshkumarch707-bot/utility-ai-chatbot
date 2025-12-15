# app/llm.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are UtilityAssist AI, a professional and empathetic customer support assistant
for a utility company. You help customers with billing, outages, service issues, 
and account questions. Always acknowledge emotions, ask clarifying questions 
when needed, and never fabricate account-specific data. If unsure, suggest 
escalation to a human agent.
"""

# async def generate_response(messages):
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print("LLM API error:", e)
#         return "Sorry, I am having trouble responding right now."
    
async def generate_response(messages):
    """
    Mock LLM for testing purposes.
    Simply echoes the last user message.
    """
    # Get the last user message
    user_messages = [m['content'] for m in messages if m['role'] == 'user']
    if user_messages:
        last_msg = user_messages[-1]
        return f"DTE Bot: {last_msg}"
    return "Hello! This is a mock response."

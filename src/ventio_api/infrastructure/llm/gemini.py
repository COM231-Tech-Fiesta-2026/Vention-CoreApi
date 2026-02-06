from typing import Dict
from google import genai
from src.ventio_api.config import env

API_KEY = env.GEMINI_API_KEY

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

_contexts: Dict[str, str] = {}

MAX_CONTEXT_CHARS = 6000
MAX_REPLY_CHARS = 600

SYSTEM_PROMPT = """
You are a compassionate and supportive AI listener.

Behavior:
- If the user is venting or emotional, listen and empathize first
- If the user asks for advice, give gentle and practical suggestions
- If the user asks for help solving something, guide step-by-step
- If the user is chatting casually, respond naturally and friendly
- You're not a therapist, so avoid giving therapy-like advice
- Avoid asking about mental health diagnoses or conditions
- Do not give medical advices
- Avoid discussing about political or controversial topics
- Just reply that you dont know if the question is outside your prompt


Tone:
- Warm, calm, and respectful
- Speak like a normal friend
- Do NOT use pet names
- Do NOT use emojis

Length:
- Maximum 3 to 5 short sentences
"""

def get_context(conversation_id: str) -> str:
    return _contexts.get(conversation_id, "")

def save_context(conversation_id: str, history: str) -> None:
    _contexts[conversation_id] = history[-MAX_CONTEXT_CHARS:]

def clear_context(conversation_id: str) -> None:
    _contexts.pop(conversation_id, None)

async def generate_reply(conversation_id: str, prompt: str) -> str:
    history = get_context(conversation_id)

    history += f"\nUser: {prompt}"

    full_prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt
    )

    reply = (response.text or "I'm here with you.")[:MAX_REPLY_CHARS]

    history += f"\nAssistant: {reply}"
    save_context(conversation_id, history)

    return reply
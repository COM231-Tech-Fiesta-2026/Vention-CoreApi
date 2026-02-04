import os
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

###############################################################################

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

router = APIRouter(prefix="/llm", tags=["LLM"])



# Memory Store (conversation retention)


_contexts: Dict[str, str] = {}

MAX_CONTEXT_CHARS = 6000
MAX_REPLY_CHARS = 600     


def get_context(conversation_id: str) -> str:
    return _contexts.get(conversation_id, "")


def save_context(conversation_id: str, history: str) -> None:
    _contexts[conversation_id] = history[-MAX_CONTEXT_CHARS:]


def clear_context(conversation_id: str) -> None:
    _contexts.pop(conversation_id, None)


#PROMPT Section for the llm behavior

SYSTEM_PROMPT = """
You are a compassionate and supportive AI listener.

Behavior:
- If the user is venting or emotional, listen and empathize first
- If the user asks for advice, give gentle and practical suggestions
- If the user asks for help solving something, guide step-by-step
- If the user is chatting casually, respond naturally and friendly

Tone:
- Warm, calm, and respectful
- Speak like a normal friend, not a therapist or parent
- Do NOT use pet names like honey, sweetie, or dear
- Do NOT use emojis or emoticons
- Avoid clichés or cheesy comfort lines
- Avoid formal or academic language

Speech style:
- Write like natural spoken conversation
- Use simple everyday words
- Keep sentences short and easy to say out loud
- Avoid long or complex explanations

Conversation style:
- Keep the conversation two-way
- Ask gentle follow-up questions when appropriate
- Do not lecture or overwhelm the user
- Give at most 1 to 2 small, practical suggestions

Length:
- Keep responses short and mobile-friendly
- Maximum 3 to 5 short sentences
- Prefer short paragraphs
- Avoid walls of text

Goal:
Help the user feel heard, understood, and supported in a natural, human way.
"""



# Schemas


class PromptRequest(BaseModel):
    conversation_id: str
    prompt: str


class PromptResponse(BaseModel):
    reply: str



# Gemini Logic


async def generate_reply(conversation_id: str, prompt: str) -> str:
    history = get_context(conversation_id)

    # Add user message
    history += f"\nUser: {prompt}"

    full_prompt = f"{SYSTEM_PROMPT}\n\nConversation so far:\n{history}"

    # IMPORTANT:
    # Older Gemini SDK supports ONLY model + contents
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt
    )

    reply = response.text or "I'm here with you."

    # Manual hard limit (instead of generation_config)
    reply = reply[:MAX_REPLY_CHARS]

    history += f"\nAssistant: {reply}"

    save_context(conversation_id, history)

    return reply



# Route


@router.post("/ask", response_model=PromptResponse)
async def ask_llm(data: PromptRequest):
    try:
        reply = await generate_reply(data.conversation_id, data.prompt)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from typing import Dict
from google import genai
from src.ventio_api.config import env, MAX_CONTEXT_CHARS, MAX_REPLY_CHARS


class GeminiClient:
    def __init__(self):
        api_key = env.GEMINI_API_KEY
        self.client = genai.Client(api_key=api_key)
        self._contexts: Dict[str, str] = {}
    
    def get_context(self, conversation_id: str) -> str:
        return self._contexts.get(conversation_id, "")
    
    def save_context(self, conversation_id: str, history: str) -> None:
        self._contexts[conversation_id] = history[-MAX_CONTEXT_CHARS:]
    
    def clear_context(self, conversation_id: str) -> None:
        self._contexts.pop(conversation_id, None)
    
    async def generate_reply(self, conversation_id: str, prompt: str, system_prompt: str) -> str:
        history = self.get_context(conversation_id)
        history += f"\nUser: {prompt}"
        full_prompt = f"{system_prompt}\n\nConversation so far:\n{history}"
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        
        reply = (response.text or "I'm here with you.")[:MAX_REPLY_CHARS]
        history += f"\nAssistant: {reply}"
        self.save_context(conversation_id, history)
        
        return reply
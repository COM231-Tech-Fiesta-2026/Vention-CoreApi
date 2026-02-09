from google import genai
from src.ventio_api.core.prompts import MAX_REPLY_CHARS
from src.ventio_api.config import env
from uuid import UUID
from ...infrastructure.database.messages_db import MessageDatabase


class GeminiClient:
    def __init__(self):
        api_key = env.LLM_API_KEY
        self.client = genai.Client(api_key=api_key)
        self.message_db = MessageDatabase()

    async def get_context(self, conversation_id: UUID) -> str:
        # return self._contexts.get(str(conversation_id), "")
        messages = await self.message_db.get_messages_by_id(conversation_id)
        print(messages)
        parts = [f"User: {m.content}\nYou: {m.reply}" for m in messages]

        return "\n\n".join(parts)

    async def generate_reply(
        self, conversation_id: UUID, prompt: str, system_prompt: str
    ) -> str:
        history = await self.get_context(conversation_id)
        history += f"\nUser: {prompt}"
        full_prompt = f"{system_prompt}\n\nConversation so far:\n{history}"

        response = self.client.models.generate_content(  # type:ignore
            model="gemini-2.5-flash", contents=full_prompt
        )

        reply = (response.text or "I'm here with you.")[:MAX_REPLY_CHARS]

        return reply

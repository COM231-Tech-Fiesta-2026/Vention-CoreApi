from src.ventio_api.infrastructure.llm.gemini import generate_reply


class LLMService:
    async def ask_llm(self, conversation_id: str, prompt: str) -> str:
        return await generate_reply(conversation_id, prompt)
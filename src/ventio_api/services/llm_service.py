from src.ventio_api.infrastructure.llm.gemini import GeminiClient
from src.ventio_api.exceptions import (
    LLMAuthenticationException,
    LLMQuotaExhaustedException,
    LLMConnectionException
)


class LLMService:
    async def ask_llm(self, conversation_id: str, prompt: str) -> str:
        gemini_client = GeminiClient()
        try:
            return await gemini_client.generate_reply(conversation_id, prompt)
        except Exception as e:
            error_msg = str(e).lower()
            
            if "401" in error_msg or "unauthenticated" in error_msg:
                raise LLMAuthenticationException("Invalid API credentials")
            elif "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                raise LLMQuotaExhaustedException("LLM quota exhausted")
            elif "connection" in error_msg or "timeout" in error_msg:
                raise LLMConnectionException("Failed to connect to LLM service")
            else:
                raise
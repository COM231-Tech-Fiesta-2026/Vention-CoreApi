from src.ventio_api.infrastructure.llm.gemini import GeminiClient
from src.ventio_api.config import SUMMARIZE_PROMPT
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


async def summarize(conversation_text: str) -> dict:
    gemini_client = GeminiClient()
    try:
        full_prompt = f"{SUMMARIZE_PROMPT}\n\nConversation:\n{conversation_text}"
        
        response = gemini_client.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        
        response_text = response.text
        
        return {
            "title": "",
            "user_feelings": "",
            "description": response_text
        }
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
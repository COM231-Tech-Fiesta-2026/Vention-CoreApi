import json
from src.ventio_api.infrastructure.llm.gemini import GeminiClient
from src.ventio_api.config import COMFORT_PROMPT, GUIDANCE_PROMPT, SUMMARIZE_PROMPT
from src.ventio_api.exceptions import (
    LLMAuthenticationException,
    LLMQuotaExhaustedException,
    LLMConnectionException
)


class LLMService:
    async def ask_llm(self, conversation_id: str, prompt: str, mode: str = "comfort") -> str:
        # Select prompt based on mode
        if mode == "comfort":
            selected_prompt = COMFORT_PROMPT
        elif mode == "guidance":
            selected_prompt = GUIDANCE_PROMPT
        else:
            # Default to comfort if mode is not recognized
            selected_prompt = COMFORT_PROMPT
        
        gemini_client = GeminiClient()
        try:
            return await gemini_client.generate_reply(conversation_id, prompt, selected_prompt)
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
        
        # Remove markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith("```"):
            # Remove opening ```json or ```
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
            # Get everything before closing ```
            response_text = response_text.split("```")[0].strip()
        
        # Parse JSON response
        parsed = json.loads(response_text)
        
        return {
            "title": parsed.get("title", ""),
            "user_feelings": parsed.get("user_feelings", ""),
            "description": parsed.get("description", "")
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
import json
from src.ventio_api.infrastructure.llm.gemini import GeminiClient
from google.genai.types import GenerateContentResponse
from src.ventio_api.core.prompts import (
    COMFORT_PROMPT,
    GUIDANCE_PROMPT,
    SUMMARIZE_PROMPT,
)
from src.ventio_api.exceptions import (
    LLMAuthenticationException,
    LLMQuotaExhaustedException,
    LLMConnectionException,
)
from ..api.schema.llm_schema import SummarizeResponse
from ..api.schema.conversation import ConversationInput
from uuid import UUID


class LLMService:
    def __init__(self):
        self.gemini_client = GeminiClient()

    async def ask_llm(self, conversation: ConversationInput) -> str:
        # Select prompt based on mode
        if conversation.mode == "vent":
            selected_prompt = COMFORT_PROMPT
        elif conversation.mode == "advice":
            selected_prompt = GUIDANCE_PROMPT
        else:
            # Default to comfort if mode is not recognized
            selected_prompt = COMFORT_PROMPT

        assert (
            conversation.conversation_key is not None
        ), "Conversation key must be generated before calling LLM"

        try:
            return await self.gemini_client.generate_reply(
                conversation.conversation_key, conversation.content, selected_prompt
            )

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

    async def summarize(self, conversation_id: UUID) -> SummarizeResponse:
        try:
            conversation_text = await self.gemini_client.get_context(conversation_id)

            full_prompt = f"{SUMMARIZE_PROMPT}\n\nConversation:\n{conversation_text}"

            response: GenerateContentResponse = (
                self.gemini_client.client.models.generate_content(  # type:ignore
                    model="gemini-2.5-flash", contents=full_prompt
                )
            )

            response_text = response.text

            # Remove markdown code blocks if present
            response_text = response_text.strip()  # type:ignore
            if response_text.startswith("```"):
                # Remove opening ```json or ```
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
                # Get everything before closing ```
                response_text = response_text.split("```")[0].strip()

            # Parse JSON response
            parsed = json.loads(response_text)

            return SummarizeResponse(
                title=parsed.get("title", ""),
                user_feelings=parsed.get("user_feelings", ""),
                description=parsed.get("description", ""),
            )
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

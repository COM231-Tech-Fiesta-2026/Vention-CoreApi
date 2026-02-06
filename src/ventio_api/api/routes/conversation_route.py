from fastapi import APIRouter
from ..schema.conversation import ConversationInput
from ...services.conversation_service import ConversationService
from ..schema.conversation import ConversationOutput, EndConversationInput

router = APIRouter(prefix="/conversation")

conversation = ConversationService()


@router.post("/{mode}")
async def create_conversation_route(
    conversation_input: ConversationInput,
) -> ConversationOutput:
    return await conversation.handle_conversation_service(conversation_input)


@router.post("/{conversation_id}/end")
async def end_conversation_route(conversation_key: EndConversationInput) -> None:
    if not conversation_key:
        raise ValueError("conversation_id is required to end conversation.")
    await conversation.end_conversation_service(conversation_key)

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ...exceptions import UserNotFoundException, ConversationNotFoundException
from ..schema.conversation import ConversationInput
from ...services.conversation_service import ConversationService
from ..schema.conversation import ConversationOutput
from uuid import UUID

router = APIRouter(prefix="/conversation")

conversation = ConversationService()


@router.post("/{mode}")
async def create_conversation_route(
    conversation_input: ConversationInput,
) -> ConversationOutput:
    try:
        return await conversation.process_message(conversation_input)
    except (UserNotFoundException, ConversationNotFoundException):
        raise


@router.post("/{conversation_id}/end")
async def end_conversation_route(conversation_id: UUID) -> None:
    if not conversation_id:
        raise HTTPException(
            status_code=400, detail="conversation_id is required to end conversation."
        )
    await conversation.close(conversation_id)


# @router.get(/):
# async def get_conversations_route(user_id: UUID):

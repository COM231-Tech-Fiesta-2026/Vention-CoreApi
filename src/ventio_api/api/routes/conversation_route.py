from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from ...exceptions import UserNotFoundException, ConversationNotFoundException
from ..schema.conversation import ConversationInput, ConversationHistory
from ..schema.auth import AccessTokenContent
from ...services.conversation_service import ConversationService
from ..schema.conversation import ConversationOutput
from ...infrastructure.auth.security import get_current_user_payload
from uuid import UUID

router = APIRouter(prefix="/conversations")

conversation = ConversationService()


@router.post("/{mode}")
async def create_conversation_route(
    conversation_input: ConversationInput,
    token: AccessTokenContent = Depends(get_current_user_payload),
) -> ConversationOutput:
    try:
        return await conversation.process_message(conversation_input, token)
    except (UserNotFoundException, ConversationNotFoundException):
        raise


@router.post("/{conversation_id}/end")
async def end_conversation_route(
    conversation_id: UUID, token: AccessTokenContent = Depends(get_current_user_payload)
) -> None:
    if not conversation_id:
        raise HTTPException(
            status_code=400, detail="conversation_id is required to end conversation."
        )
    await conversation.close(conversation_id)


@router.get("/")
async def get_conversations_route(
    token: AccessTokenContent = Depends(get_current_user_payload),
) -> list[ConversationHistory]:

    conversations = await conversation.get(token)

    if conversations == []:
        raise HTTPException(status_code=404, detail="There's no conversation exists.")

    return conversations

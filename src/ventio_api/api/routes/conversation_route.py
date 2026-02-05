from fastapi import APIRouter
from ..schema.conversation import ConversationInput
from uuid import UUID
from ...services.conversation_service import ConversationService

router = APIRouter(prefix="/conversation")

conversation = ConversationService()


@router.post("/{mode}")
async def create_conversation_route(payload: ConversationInput):
    return await conversation.handle_conversation_service(payload.model_dump())


@router.post("/{conversation_id}/end")
async def end_conversation_route(conversation_id: UUID):
    return await conversation.end_conversation_service(conversation_id)

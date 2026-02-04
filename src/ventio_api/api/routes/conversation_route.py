from fastapi import APIRouter
from ..schema.converstation import ConversationMode
from uuid import UUID

from ...services.conversation_service import (
    create_conversation_service,
    end_conversation_service,
)

router = APIRouter(prefix="/conversation")


@router.post("/{mode}")
async def create_conversation_route(
    mode: ConversationMode, conversation_id: UUID | None = None
):
    return await create_conversation_service(mode, conversation_id)


@router.post("/{conversation_id}/end")
async def end_conversation_route(conversation_id: UUID):
    return await end_conversation_service(conversation_id)

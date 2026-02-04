from fastapi import APIRouter
from src.ventio_api.api.routes.conversation_route import router as conversation_router

router = APIRouter(prefix="/api/v1")

router.include_router(conversation_router)

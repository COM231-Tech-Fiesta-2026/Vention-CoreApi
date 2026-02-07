from fastapi import APIRouter, Depends
from src.ventio_api.api.routes.conversation_route import router as conversation_router
from src.ventio_api.infrastructure.auth.security import oauth2_scheme
from src.ventio_api.api.routes import user_routes, auth_routes


router = APIRouter(prefix="/api/v1")

router.include_router(conversation_router)
router.include_router(auth_routes.router, tags=["Auth"])
router.include_router(
    user_routes.router, tags=["User"], dependencies=[Depends(oauth2_scheme)]
)

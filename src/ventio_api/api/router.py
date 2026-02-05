from fastapi import APIRouter, Depends
from src.ventio_api.infrastructure.auth.security import oauth2_scheme
from src.ventio_api.api.routes import user_routes, auth_routes

api_router = APIRouter()

api_router.include_router(auth_routes.router, tags=["Auth"])
api_router.include_router(
    user_routes.router, 
    tags=["User"],
    dependencies=[Depends(oauth2_scheme)] 
)
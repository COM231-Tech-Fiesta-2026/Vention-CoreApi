from fastapi import APIRouter, Depends
from src.ventio_api.infrastructure.database.users_db import users_db
from src.ventio_api.services.user_service import UserService
from src.ventio_api.infrastructure.auth.security import get_current_user_claims
from src.ventio_api.api.schema.user import UserProfile, UserUpdate

router = APIRouter()

def get_user_service():
    return UserService(users_db)

@router.get("/user", response_model=UserProfile)
async def get_user_profile(
    claims: dict = Depends(get_current_user_claims),
    user_service: UserService = Depends(get_user_service)):
    return await user_service.get_profile(claims["user_id"])

@router.put("/user", response_model=UserProfile)
async def update_user_profile(
    update_data: UserUpdate, 
    claims: dict = Depends(get_current_user_claims),
    user_service: UserService = Depends(get_user_service)):
    return await user_service.update_profile(claims["user_id"], update_data)
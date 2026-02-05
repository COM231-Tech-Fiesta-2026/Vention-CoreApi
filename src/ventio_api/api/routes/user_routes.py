from fastapi import APIRouter, Depends, HTTPException, Request
from src.ventio_api.infrastructure.database.users_db import users_db
from src.ventio_api.services.user_service import UserService
from src.ventio_api.api.schema.user import UserProfile, UserUpdate
from src.ventio_api.exceptions import NotFoundException

router = APIRouter()

def get_user_service():
    return UserService(users_db)

@router.get("/user", response_model=UserProfile)
async def get_user_profile(
    request: Request,
    user_service: UserService = Depends(get_user_service)):
    try:
        user_id = request.state.user_id 
        
        print(f"DEBUG: Looking for user_id: {user_id} (Type: {type(user_id)})")
        return await user_service.get_profile(user_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/user", response_model=UserProfile)
async def update_user_profile(
    update_data: UserUpdate, 
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user_id = request.state.user_id
        return await user_service.update_profile(user_id, update_data)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
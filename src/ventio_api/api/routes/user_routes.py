from fastapi import APIRouter, Depends, HTTPException, status
from src.ventio_api.api.schema.auth import TokenPayload
from src.ventio_api.infrastructure.database.users_db import users_db
from src.ventio_api.services.user_service import UserService
from src.ventio_api.api.schema.user import UserProfile, UserUpdate
from src.ventio_api.exceptions import NotFoundException, AuthorizationException
from src.ventio_api.infrastructure.auth.security import get_current_user_payload

router = APIRouter()

def get_user_service():
    return UserService(users_db)

@router.get("/user", response_model=UserProfile)
async def get_user_profile(
    payload: TokenPayload = Depends(get_current_user_payload),
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.get_profile(payload.user_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except AuthorizationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An error occurred while retrieving the profile."
        )

@router.put("/user", response_model=UserProfile)
async def update_user_profile(
    form_data: UserUpdate,
    payload: TokenPayload = Depends(get_current_user_payload),
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.update_profile(payload.user_id, form_data)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update profile."
        )
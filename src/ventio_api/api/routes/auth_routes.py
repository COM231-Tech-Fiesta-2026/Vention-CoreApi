from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.ventio_api.infrastructure.database.users_db import users_db
from src.ventio_api.services.auth_service import AuthService
from src.ventio_api.api.schema.user import UserSignup

router = APIRouter()

def get_auth_service():
    return AuthService(users_db)

@router.post("/signup")
async def signup(
    user: UserSignup, 
    auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.signup(user)

@router.post("/signin")
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.signin(form_data.username, form_data.password)
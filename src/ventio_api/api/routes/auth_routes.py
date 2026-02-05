from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.ventio_api.infrastructure.database.users_db import users_db
from src.ventio_api.services.auth_service import AuthService
from src.ventio_api.api.schema.user import UserSignup
from src.ventio_api.api.schema.auth import Token
from src.ventio_api.exceptions import UsernameAlreadyExists, InvalidCredentials

router = APIRouter()

def get_auth_service():
    return AuthService(users_db)

@router.post("/signup")
async def signup(
    user: UserSignup, 
    auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.signup(user)
    except UsernameAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin", response_model=Token)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.signin(form_data.username, form_data.password)
    
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
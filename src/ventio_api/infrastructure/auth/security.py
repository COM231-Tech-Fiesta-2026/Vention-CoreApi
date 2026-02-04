from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.ventio_api.config import settings
from src.ventio_api.api.schema.user import TokenPayload
from pydantic import ValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_tokens(user_id: str, name: str):
    """
    Generates both Access and Refresh tokens with your specific claims.
    """
    access_claims = {
        "user_id": user_id,
        "name": name,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    }
    access_token = jwt.encode(access_claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    refresh_claims = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    }
    refresh_token = jwt.encode(refresh_claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }


async def get_current_user_claims(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        user_id: str = payload.get("user_id")
        name: str = payload.get("name")
        
        if user_id is None or name is None:
            raise HTTPException(status_code=401, detail="Invalid token claims")
            
        return {"user_id": user_id, "name": name}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_refresh_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        if token_data.type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return token_data
    except (ValidationError, JWTError):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
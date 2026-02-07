from datetime import datetime, timedelta, UTC
from typing import Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from src.ventio_api.config import env
from src.ventio_api.api.schema.auth import TokenPayload
from src.ventio_api.exceptions import InvalidToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/signin")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_tokens(user_id: str, name: str) -> dict[str, str]:
    """
    Generates tokens using 'sub' so it matches your Schema alias.
    """
    access_claims: dict[str, Any] = {
        "sub": user_id,
        "name": name,
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(days=env.ACCESS_TOKEN_EXPIRE_DAYS),
    }
    access_token = jwt.encode(access_claims, env.SECRET_KEY, algorithm=env.ALGORITHM)

    refresh_claims: dict[str, Any] = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.now(UTC) + timedelta(days=env.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    refresh_token = jwt.encode(refresh_claims, env.SECRET_KEY, algorithm=env.ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def decode_token(token: str, expected_type: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])

        # Pydantic reads 'sub' from token and puts it into 'user_id'
        token_data = TokenPayload(**payload)

        if token_data.type != expected_type:
            raise InvalidToken(f"Token type must be '{expected_type}'")
        return token_data

    except (JWTError, ValidationError):
        raise InvalidToken("Could not validate credentials")


async def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    token_data = decode_token(token, expected_type="access")
    return token_data


def verify_refresh_token(token: str) -> TokenPayload:
    return decode_token(token, expected_type="refresh")

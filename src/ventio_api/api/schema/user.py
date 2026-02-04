from pydantic import BaseModel, validator
from typing import Optional, Literal
from datetime import datetime

class UserBase(BaseModel):
    name: str
    username: str

class User(BaseModel):
    user_id: str
    name: str
    username: str
    pass_hash: str
    bday: str
    age: str
    gender: str
    bio: Optional[str] = ""
    created_at: datetime

class UserSignup(BaseModel):
    name: str
    username: str
    password: str
    bday: str 
    gender: Literal['M', 'F'] 

    @validator('bday')
    def validate_bday(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Birthday must be in YYYY-MM-DD format")

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    bday: Optional[str] = None
    gender: Optional[Literal['M', 'F']] = None
    bio: Optional[str] = ""

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    name: str
    bday: str
    gender: str
    bio: Optional[str] = ""

class TokenPayload(BaseModel):
    user_id: str
    name: Optional[str] = None
    type: str
    exp: int
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from uuid import UUID
from datetime import date, datetime

class UserBase(BaseModel):
    name: str
    username: str

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
    name: str
    bday: str
    gender: Literal['M', 'F']
    bio: Optional[str] = ""

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    name: str
    bday: str
    gender: str
    bio: Optional[str] = ""
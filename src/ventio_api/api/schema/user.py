from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date


class UserSignup(BaseModel):
    name: str
    username: str
    password: str
    birthday: date
    gender: Literal["M", "F"]


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[Literal["M", "F"]] = None
    bio: Optional[str] = ""


class UserProfile(BaseModel):
    name: str
    birthday: date
    gender: Literal["M", "F"]
    bio: Optional[str] = ""

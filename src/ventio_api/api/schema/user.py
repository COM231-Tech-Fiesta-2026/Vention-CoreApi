from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID

class UserGender(str, Enum):
	MALE = "MALE"
	FEMALE = "FEMALE"

class User(BaseModel):
	user_id: UUID = Field(...)
	name: str = Field(...)
	username: str = Field(...)
	pass_hash: str = Field(...)
	bday: str = Field(...)
	age: int = Field(...)
	gender: UserGender = Field(...)

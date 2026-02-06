from pydantic import AliasChoices, BaseModel, Field
from datetime import date, datetime
from typing import Literal, Optional, Union
import uuid

class User(BaseModel):
    user_id: Union[uuid.UUID, str] = Field(alias="id")
    name: str
    username: str
    pass_hash: str
    birthday: date = Field(validation_alias=AliasChoices('birthday', 'bday'))
    age: int
    gender: Literal['M', 'F']
    bio: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
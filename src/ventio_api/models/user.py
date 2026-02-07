from pydantic import AliasChoices, BaseModel, Field
from datetime import date, datetime, UTC
from typing import Literal
from uuid import UUID


class User(BaseModel):
    user_id: UUID = Field(alias="id")
    name: str
    username: str
    pass_hash: str
    birthday: date = Field(validation_alias=AliasChoices("birthday", "bday"))
    age: int
    gender: Literal["M", "F"]
    bio: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        populate_by_name = True

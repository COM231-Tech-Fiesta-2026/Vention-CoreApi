from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    user_id: UUID = Field(alias="sub") # Maps 'sub' in token to 'user_id' in code
    name: Optional[str] = None
    type: str      # e.g., "access" or "refresh"
    exp: int

    class Config:
        populate_by_name = True # Allows populating by either 'sub' or 'user_id'       
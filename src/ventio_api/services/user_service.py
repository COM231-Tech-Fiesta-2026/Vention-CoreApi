from uuid import UUID
from src.ventio_api.api.schema.user import UserUpdate
from src.ventio_api.models.user import User
from ..infrastructure.database.users_db import UserDatabase


class UserService:
    def __init__(self, user_db: UserDatabase):
        self.user_db = user_db

    async def get_profile(self, user_id: UUID) -> User:
        if not user_id:
            raise ValueError("Invalid request: User ID missing")
        user = await self.user_db.get_user_by_id(user_id)
        return user

    async def update_profile(self, user_id: UUID, update_data: UserUpdate) -> User:
        if not user_id:
            raise ValueError("Invalid request: User ID missing")
        return await self.user_db.update_user_by_id(user_id, update_data)

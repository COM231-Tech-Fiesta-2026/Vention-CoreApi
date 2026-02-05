from src.ventio_api.api.schema.user import UserUpdate
from src.ventio_api.exceptions import NotFoundException

class UserService:
    def __init__(self, user_db):
        self.user_db = user_db

    async def get_profile(self, user_id: str):
        user = await self.user_db.get_user_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return user
    

    async def update_profile(self, user_id: str, update_data: UserUpdate):
        await self.user_db.update_user_by_id(user_id, update_data)
        user = await self.user_db.get_user_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")        
        return user
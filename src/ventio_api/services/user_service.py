from fastapi import HTTPException
from src.ventio_api.api.schema.user import UserUpdate
from src.ventio_api.core.utils import calculate_age
from src.ventio_api.exceptions import NotFoundException

class UserService:
    def __init__(self, user_db):
        self.user_db = user_db

    async def get_profile(self, user_id: str):
        try:
            user = self.user_db.get(user_id=user_id)
            return {
                "name": user.name,
                "bday": user.bday,
                "gender": user.gender,
                "bio": user.bio
            }
        except NotFoundException:
            raise HTTPException(status_code=404, detail="User not found")

    async def update_profile(self, user_id: str, update_data: UserUpdate):
        age = calculate_age(update_data.bday)
        
        update_fields = {
            "name": update_data.name,
            "bday": update_data.bday,
            "age": age,
            "gender": update_data.gender,
            "bio": update_data.bio
        }
        
        try:
            self.user_db.partial_update(set=update_fields, user_id=user_id)
            return update_fields
        except NotFoundException:
            raise HTTPException(status_code=404, detail="User not found")
from src.ventio_api.core.utils import calculate_age
from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.user import User, UserUpdate

class UserDatabase(BaseDatabase[User]):
	collection_name = "users"
	model = User

	async def get_by_username(self, username: str) -> User:
		return self.get(username=username)

	async def update_user_by_id(self, user_id: str, updates: UserUpdate):
				update_data = updates.model_dump(exclude_unset=True)
				if "bday" in update_data and update_data["bday"]:
					update_data["age"] = calculate_age(update_data["bday"])
				if update_data:
					return self.partial_update(set=update_data, user_id=user_id)
	
users_db = UserDatabase()

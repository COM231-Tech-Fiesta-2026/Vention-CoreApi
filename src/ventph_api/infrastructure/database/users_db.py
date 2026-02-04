from src.ventph_api.infrastructure.database.base_database import BaseDatabase
from src.ventph_api.api.schema.user import User

class UserDatabase(BaseDatabase[User]):
	collection_name = "users"
	model = User

user_db = UserDatabase()
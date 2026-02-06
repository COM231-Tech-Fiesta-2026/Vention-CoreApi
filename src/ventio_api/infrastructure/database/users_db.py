from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.user import User


class UserDatabase(BaseDatabase[User]):
    collection_name = "users"
    model = User

    def __init__(self):
        super().__init__()

import uuid
from datetime import datetime
from src.ventio_api.api.schema.user import UserSignup, User
from src.ventio_api.core.utils import calculate_age
from src.ventio_api.infrastructure.auth.security import get_password_hash, create_tokens, verify_password
from src.ventio_api.exceptions import NotFoundException, UsernameAlreadyExists, InvalidCredentials
from src.ventio_api.infrastructure.database.users_db import users_db

class AuthService:
    def __init__(self, user_db):
        self.user_db = user_db

    async def signup(self, user: UserSignup):
        try:
            self.user_db.get_by_username(user.username)
            raise UsernameAlreadyExists(f"Username {user.username} is already taken")
        except NotFoundException:

            pass

        user_id = str(uuid.uuid4())
        age = calculate_age(user.bday)
        
        new_user = User(
            user_id=user_id,
            name=user.name,
            username=user.username,
            pass_hash=get_password_hash(user.password),
            bday=user.bday,
            age=age,
            gender=user.gender,
            bio="",
            created_at=datetime.utcnow()
        )

        await self.user_db.insert(new_user)

        return create_tokens(user_id=user_id, name=user.name)
    
    
    async def signin(self, username: str, password: str):
        try:
            user = await self.user_db.get_by_username(username)
        except NotFoundException:
            raise InvalidCredentials("Incorrect username or password")

        if not verify_password(password, user.pass_hash):
            raise InvalidCredentials("Incorrect username or password")

        return create_tokens(user_id=user.user_id, name=user.name)

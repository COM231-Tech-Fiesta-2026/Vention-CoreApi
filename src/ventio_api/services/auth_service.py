import uuid
from datetime import datetime, UTC
from src.ventio_api.models.user_model import User
from src.ventio_api.api.schema.user import UserSignup
from src.ventio_api.core.utils import calculate_age
from ..infrastructure.database.users_db import UserDatabase
from src.ventio_api.infrastructure.auth.security import (
    get_password_hash,
    create_tokens,
    verify_password,
)
from src.ventio_api.exceptions import (
    UserNotFoundException,
    UsernameAlreadyExists,
    InvalidCredentials,
)


class AuthService:
    def __init__(self, user_db: UserDatabase):
        self.user_db = user_db

    async def signup(self, user: UserSignup):
        existing_user = await self.user_db.get_by_username(user.username)

        if existing_user:
            raise UsernameAlreadyExists(f"Username {user.username} is already taken")

        user_id_obj = uuid.uuid4()
        age = calculate_age(user.birthday)

        new_user = User(
            id=user_id_obj,
            name=user.name,
            username=user.username,
            pass_hash=get_password_hash(user.password),
            birthday=user.birthday,
            age=age,
            gender=user.gender,
            bio="",
            created_at=datetime.now(UTC),
        )

        await self.user_db.create(new_user)

        return create_tokens(user_id=str(user_id_obj), name=user.name)

    async def signin(self, username: str, password: str):
        user = await self.user_db.get_by_username(username)

        if user is None:
            raise UserNotFoundException("User does not exist.")
        if not verify_password(password, user.pass_hash):
            raise InvalidCredentials("Incorrect username or password")

        return create_tokens(user_id=str(user.user_id), name=user.name)

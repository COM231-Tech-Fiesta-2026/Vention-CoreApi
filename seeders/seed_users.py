from src.ventio_api.models.user import User
from uuid import uuid4
from datetime import date
from src.ventio_api.infrastructure.database.users_db import UserDatabase
import asyncio


SEED_USERS = [
    User(
        id=uuid4(),
        name="Alice Smith",
        username="alice",
        pass_hash="hashed_password_1",
        birthday=date(1995, 1, 1),
        age=28,
        gender="F",
    ),
    User(
        id=uuid4(),
        name="Bob Johnson",
        username="bob",
        pass_hash="hashed_password_2",
        birthday=date(1995, 5, 10),
        age=31,
        gender="M",
    ),
]


async def seed_users():
    user_db = UserDatabase()
    print("Seeding users...")
    users = await user_db.collection.insert_many(
        [user.model_dump(mode="json") for user in SEED_USERS]
    )
    print("Users seeded successfully!: ", users)


async def get_seed_users():
    user_db = UserDatabase()
    user = await user_db.get(user_id="a425dca5-06e1-421d-a1f5-54ea2bd2a0c1")
    return user


if __name__ == "__main__":
    asyncio.run(seed_users())

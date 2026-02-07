from src.ventio_api.models.user_model import User
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
    user = await user_db.get(user_id="4a1108c0-309a-45b8-8e3e-b90c21e23da5")
    return user


if __name__ == "__main__":
    asyncio.run(seed_users())

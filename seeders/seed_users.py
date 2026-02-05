from src.ventio_api.api.schema.user import User, UserGender
from uuid import uuid4, UUID
from src.ventio_api.infrastructure.database.users_db import UserDatabase
import asyncio


SEED_USERS = [
    User(
        user_id=str(uuid4()),
        name="Alice Smith",
        username="alice",
        pass_hash="hashed_password_1",
        bday="1995-01-01",
        age=28,
        gender=UserGender.FEMALE,
    ),
    User(
        user_id=str(uuid4()),
        name="Bob Johnson",
        username="bob",
        pass_hash="hashed_password_2",
        bday="1992-05-10",
        age=31,
        gender=UserGender.MALE,
    ),
]


async def seed_users():
    user_db = UserDatabase()
    print("Seeding users...")
    users = await user_db.collection.insert_many(
        [user.model_dump() for user in SEED_USERS]
    )
    print("Users seeded successfully!: ", users)


async def get_seed_users():
    user_db = UserDatabase()
    user = await user_db.get(user_id=UUID("97cec983-4f62-41ca-b834-76cacdd7d08f"))
    return user.model_dump()


if __name__ == "__main__":
    asyncio.run(seed_users())

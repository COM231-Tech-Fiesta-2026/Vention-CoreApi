from src.ventio_api.api.schema.user import User, UserGender
from uuid import uuid4
from src.ventio_api.infrastructure.database.users_db import user_db
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
	print("Seeding users...")
	users = await user_db.collection.insert_many([user.model_dump() for user in SEED_USERS])
	print("Users seeded successfully!: ", users)

if __name__ == "__main__":
    asyncio.run(seed_users())
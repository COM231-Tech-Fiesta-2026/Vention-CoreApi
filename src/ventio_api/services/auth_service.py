import uuid
from datetime import datetime
from fastapi import HTTPException
from src.ventio_api.api.schema.user import UserSignup, User
from src.ventio_api.core.utils import calculate_age
from src.ventio_api.infrastructure.auth.security import get_password_hash, create_tokens, verify_password
from src.ventio_api.exceptions import NotFoundException

class AuthService:
    def __init__(self, user_db):
        self.user_db = user_db

    async def signup(self, user: UserSignup):
        try:
            self.user_db.get(username=user.username)
            raise HTTPException(status_code=409, detail="Username already taken")
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

        self.user_db.insert(new_user)

        return create_tokens(user_id=user_id, name=user.name)
    
    
    async def signin(self, username: str, password: str):
        try:
            db_user = self.user_db.get(username=username)
            
            if not verify_password(password, db_user.pass_hash):
                raise HTTPException(status_code=401, detail="Wrong Username or Password")
            
            return create_tokens(user_id=db_user.user_id, name=db_user.name)
            
        except NotFoundException:
            raise HTTPException(status_code=401, detail="Wrong Username or Password")

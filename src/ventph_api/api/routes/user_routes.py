from fastapi import APIRouter, HTTPException, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from src.ventph_api.infrastructure.database.mongo import users_collection
from src.ventph_api.infrastructure.auth.security import (
    get_password_hash, 
    verify_password, 
    create_tokens, 
    get_current_user_claims,
    verify_refresh_token
)
from src.ventph_api.api.schema.users import UserSignup, UserProfile, UserUpdate, Token
import uuid
from datetime import datetime

router = APIRouter()

def calculate_age(bday_str: str) -> str:
    birth_date = datetime.strptime(bday_str, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return str(age)


@router.post("/signup")
async def signup(user: UserSignup):
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=409, detail="Username already taken")

    user_id = str(uuid.uuid4())
    age = calculate_age(user.bday)
    
    new_user = {
        "user_id": user_id,
        "name": user.name,
        "username": user.username,
        "pass_hash": get_password_hash(user.password),
        "bday": user.bday,
        "age": age,
        "gender": user.gender,
        "bio": "",
        "created_at": datetime.utcnow()
    }

    await users_collection.insert_one(new_user)

    return create_tokens(user_id=user_id, name=user.name)


@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await users_collection.find_one({"username": form_data.username})
    
    if not db_user or not verify_password(form_data.password, db_user["pass_hash"]):
        raise HTTPException(status_code=401, detail="Wrong Username or Password")
    
    return create_tokens(user_id=db_user["user_id"], name=db_user["name"])


@router.get("/user", response_model=UserProfile)
async def get_user_profile(claims: dict = Depends(get_current_user_claims)):
    user_data = await users_collection.find_one({"user_id": claims["user_id"]})
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "name": user_data["name"],
        "bday": user_data["bday"],
        "gender": user_data["gender"],
        "bio": user_data.get("bio", "")
    }

@router.put("/user", response_model=UserProfile)
async def update_user_profile(update_data: UserUpdate, claims: dict = Depends(get_current_user_claims)):
    age = calculate_age(update_data.bday)
    
    update_fields = {
        "name": update_data.name,
        "bday": update_data.bday,
        "age": age,
        "gender": update_data.gender,
        "bio": update_data.bio
    }
    
    result = await users_collection.update_one(
        {"user_id": claims["user_id"]},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return update_fields
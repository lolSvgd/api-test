from app.models.user import UserInDB, UserCreate, UserInDB
from app.db.mongo import db
from app.core.security import verify_password, hash_password

async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if user and verify_password(password, user["hashed_password"]):
        return UserInDB(**user)
    return None

async def create_user(user_in: UserCreate) -> UserInDB:
    user_dict = user_in.dict()
    user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
    result = await db.users.insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    return UserInDB(**user_dict)

async def get_user_by_email(email: str):
    data = await db.users.find_one({"email": email})
    return UserInDB(**data) if data else None
from fastapi import Depends, APIRouter, HTTPException
from app.core.deps import get_current_user
from app.models.user import UserCreate, UserPublic
from app.services.user_service import create_user, get_user_by_email

router = APIRouter()

@router.get("/me", response_model=UserPublic)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=UserPublic)
async def register(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_created = await create_user(user)
    return UserPublic(id=str(user_created.id), email=user_created.email, username=user_created.username)

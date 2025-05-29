import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from bson import ObjectId
from app.core.security import verify_token
from app.db.mongo import db
from app.models.user import UserInDB

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    logger.debug("Received token for validation.")
    try:
        payload = verify_token(token)
        logger.debug("Token payload: %s", payload)
        user_id = payload.get("sub")
        if user_id is None:
            logger.warning("Token is valid but missing 'sub' claim.")
            raise HTTPException(status_code=401, detail="Invalid token: no subject")
    except PyJWTError as e:
        logger.error("Token verification failed: %s", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
    
    logger.debug("Fetching user from DB with id: %s", user_id)
    
    # Convert string ID to ObjectId
    try:
        object_id = ObjectId(user_id)
    except Exception as e:
        logger.error("Invalid ObjectId format: %s", str(e))
        raise HTTPException(status_code=401, detail="Invalid user ID format")
    
    user = await db.users.find_one({"_id": object_id})
    if not user:
        logger.warning("No user found in DB for id: %s", user_id)
        raise HTTPException(status_code=401, detail="User not found")
    
    # Convert ObjectId to string before creating the model
    if "_id" in user:
        user["_id"] = str(user["_id"])
    
    logger.info("User authenticated successfully: %s", user_id)
    return UserInDB(**user)

from pydantic import BaseModel, EmailStr, Field, GetJsonSchemaHandler, constr, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import Optional, Any
from bson import ObjectId

class PyObjectId(ObjectId):
# handles MongoDB ObjectId serialization.
    @classmethod
    def __get_pydantic_core_schema__(
        cls, 
        source_type: Any, 
        handler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, 
        core_schema: core_schema.CoreSchema, 
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class UserBase(BaseModel):
# Base user model.
    username: constr(min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")   # type: ignore
    email: EmailStr


class UserCreate(UserBase):
# User registration model.
    password: constr(min_length=8, max_length=64)  # type: ignore


class UserInDB(UserBase):
#User model for database operations.
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str


    model_config = ConfigDict(
        populate_by_name=True, 
        arbitrary_types_allowed=True
    )


class UserPublic(UserBase):
# Public user model for API responses without sensitive data.
    id: str

    @classmethod
    def from_user_in_db(cls, user_in_db: UserInDB) -> "UserPublic":
        """Convert UserInDB to UserPublic"""
        return cls(
            id=str(user_in_db.id),
            username=user_in_db.username,
            email=user_in_db.email
        )


class LoginRequest(BaseModel):
# Login request model.
    email: EmailStr
    password: str

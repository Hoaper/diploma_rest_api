from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class BudgetRange(BaseModel):
    min: int
    max: int

class SocialLinks(BaseModel):
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None

class User(BaseModel):
    userId: Optional[str] = None
    name: Optional[str] = None
    email: EmailStr
    admin: bool = False
    password: Optional[str] = None
    surname: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    phone: Optional[str] = None
    nationality: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    university: Optional[str] = None
    studentId_number: Optional[str] = None
    group: Optional[str] = None
    roommate_preferences: Optional[str] = None
    language_preferences: Optional[List[str]] = None
    budget_range: Optional[Dict[str, int]] = None
    avatar_url: Optional[str] = None
    id_document_url: Optional[str] = None
    document_verified: Optional[bool] = False
    social_links: Optional[Dict[str, str]] = None
    is_landlord: Optional[bool] = False
    is_verified_landlord: Optional[bool] = False
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        from_attributes = True
        json_encoders = {
            ObjectId: str
        }

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return None
        id = data.pop('_id', None)
        return cls(**dict(data, userId=str(id))) 
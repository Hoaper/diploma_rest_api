from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint
from enum import Enum
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

class ReviewType(str, Enum):
    APARTMENT = "apartment"
    USER = "user"

class Review(BaseModel):
    reviewId: Optional[str] = None
    reviewerId: str
    targetId: str  # apartmentId or userId
    review_type: ReviewType
    rating: conint(ge=1, le=5)  # Rating from 1 to 5
    text: str
    created_at: datetime
    updated_at: datetime
    is_verified: bool = False  # For verified stays

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return None
        id = data.pop('_id', None)
        return cls(**dict(data, reviewId=str(id))) 
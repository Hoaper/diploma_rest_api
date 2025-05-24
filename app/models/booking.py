from datetime import datetime
from typing import Optional
from pydantic import BaseModel
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

class BookingStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Booking(BaseModel):
    bookingId: Optional[str] = None
    apartmentId: str
    userId: str
    message: Optional[str] = None
    status: BookingStatus = BookingStatus.PENDING
    check_in_date: datetime
    check_out_date: datetime
    created_at: datetime
    updated_at: datetime
    payment_status: str = "pending"  # pending, completed, refunded
    paymentId: Optional[str] = None

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
        return cls(**dict(data, bookingId=str(id))) 
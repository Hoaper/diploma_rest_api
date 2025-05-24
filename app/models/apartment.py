from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
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

class Address(BaseModel):
    street: str
    house_number: str
    apartment_number: str
    entrance: Optional[str] = None
    has_intercom: bool = False
    landmark: Optional[str] = None

class Apartment(BaseModel):
    apartmentId: Optional[str] = None
    ownerId: str
    apartment_name: str
    description: str
    address: Address
    district_name: str
    latitude: float
    longitude: float
    price_per_month: int
    area: float
    kitchen_area: float
    floor: int
    number_of_rooms: int
    max_users: int
    available_from: datetime
    available_until: datetime
    university_nearby: str
    pictures: List[str]
    is_promoted: bool = False
    is_pet_allowed: bool = False
    rental_type: str  # "room" or "apartment"
    roommate_preferences: Optional[str] = None
    included_utilities: List[str]
    rules: List[str]
    contact_phone: str
    contact_telegram: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

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
        return cls(**dict(data, apartmentId=str(id))) 
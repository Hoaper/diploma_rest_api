from typing import Optional, List
from datetime import datetime
from models.booking import Booking, BookingStatus
from repositories.base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class BookingRepository(BaseRepository[Booking]):
    def __init__(self, client: AsyncIOMotorClient):
        self.db = client.get_database("diploma")
        self.collection = self.db["Bookings"]

    async def create(self, entity: Booking) -> Booking:
        try:
            entity_dict = entity.dict()
            entity_dict["createdAt"] = datetime.utcnow()
            entity_dict["updatedAt"] = datetime.utcnow()
            result = await self.collection.insert_one(entity_dict)
            entity_dict["bookingId"] = str(result.inserted_id)
            return Booking(**entity_dict)
        except Exception as e:
            print(e)
            return None

    async def get_by_id(self, entity_id: str) -> Optional[Booking]:
        try:
            result = await self.collection.find_one({"_id": ObjectId(entity_id)})
            if result:
                result["bookingId"] = str(result["_id"])
                del result["_id"]
                return Booking(**result)
            return None
        except Exception as e:
            print(e)
            return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Booking]:
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            bookings = []
            async for document in cursor:
                document["bookingId"] = str(document["_id"])
                del document["_id"]
                bookings.append(Booking(**document))
            return bookings
        except Exception as e:
            print(e)
            return []

    async def update(self, entity_id: str, entity: Booking) -> Optional[Booking]:
        try:
            entity_dict = entity.dict(exclude_unset=True)
            entity_dict["updatedAt"] = datetime.utcnow()
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(entity_id)},
                {"$set": entity_dict},
                return_document=True
            )
            if result:
                result["bookingId"] = str(result["_id"])
                del result["_id"]
                return Booking(**result)
            return None
        except Exception as e:
            print(e)
            return None

    async def delete(self, entity_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(entity_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(e)
            return False

    async def get_by_user(self, userId: str) -> List[Booking]:
        try:
            cursor = self.collection.find({"userId": userId})
            bookings = []
            async for document in cursor:
                document["bookingId"] = str(document["_id"])
                del document["_id"]
                bookings.append(Booking(**document))
            return bookings
        except Exception as e:
            print(e)
            return []

    async def get_by_apartment(self, apartment_id: str) -> List[Booking]:
        try:
            cursor = self.collection.find({"apartmentId": apartment_id})
            bookings = []
            async for document in cursor:
                document["bookingId"] = str(document["_id"])
                del document["_id"]
                bookings.append(Booking(**document))
            return bookings
        except Exception as e:
            print(e)
            return []

    async def get_by_status(
        self,
        status: BookingStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Booking]:
        try:
            cursor = self.collection.find({"status": status}).skip(skip).limit(limit)
            bookings = []
            async for document in cursor:
                document["bookingId"] = str(document["_id"])
                del document["_id"]
                bookings.append(Booking(**document))
            return bookings
        except Exception as e:
            print(e)
            return []

    async def update_status(
        self,
        booking_id: str,
        status: BookingStatus
    ) -> Optional[Booking]:
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(booking_id)},
                {
                    "$set": {
                        "status": status,
                        "updatedAt": datetime.utcnow()
                    }
                },
                return_document=True
            )
            if result:
                result["bookingId"] = str(result["_id"])
                del result["_id"]
                return Booking(**result)
            return None
        except Exception as e:
            print(e)
            return None

    async def check_availability(
        self,
        apartment_id: str,
        check_in: datetime,
        check_out: datetime
    ) -> bool:
        try:
            # Check if there are any overlapping bookings
            overlapping_booking = await self.collection.find_one({
                "apartmentId": apartment_id,  # <-- исправлено
                "status": {"$in": ["pending", "accepted"]},
                "$or": [
                    {
                        "check_in_date": {"$lte": check_out},
                        "check_out_date": {"$gte": check_in}
                    }
                ]
            })
            return overlapping_booking is None
        except Exception as e:
            print(e)
            return False 
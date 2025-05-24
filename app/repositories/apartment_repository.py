from typing import Optional, List
from datetime import datetime
from models.apartment import Apartment
from repositories.base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

class ApartmentRepository(BaseRepository[Apartment]):
    def __init__(self, client: AsyncIOMotorClient):
        self.db = client.get_database("diploma")
        self.collection = self.db["Apartments"]

    async def create(self, entity: Apartment) -> Apartment:
        try:
            entity_dict = jsonable_encoder(entity)  # <--- исправлено
            entity_dict["createdAt"] = datetime.utcnow()
            entity_dict["updatedAt"] = datetime.utcnow()
            result = await self.collection.insert_one(entity_dict)
            entity_dict["apartmentId"] = str(result.inserted_id)
            return Apartment(**entity_dict)
        except Exception as e:
            print(e)
            return None

    async def get_by_id(self, entity_id: str) -> Optional[Apartment]:
        try:
            result = await self.collection.find_one({"_id": ObjectId(entity_id)})
            return Apartment.from_mongo(result)
        except Exception as e:
            print(e)
            return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Apartment]:
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            apartments = []
            async for document in cursor:
                apartments.append(Apartment.from_mongo(document))
            return apartments
        except Exception as e:
            print(e)
            return []

    async def update(self, entity_id: str, entity: Apartment) -> Optional[Apartment]:
        try:
            entity_dict = entity.dict(exclude_unset=True)
            entity_dict["updated_at"] = datetime.utcnow()
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(entity_id)},
                {"$set": entity_dict},
                return_document=True
            )
            return Apartment.from_mongo(result)
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

    async def get_by_owner(self, owner_id: str) -> List[Apartment]:
        try:
            cursor = self.collection.find({"ownerId": owner_id})
            apartments = []
            async for document in cursor:
                apartments.append(Apartment.from_mongo(document))
            return apartments
        except Exception as e:
            print(e)
            return []

    async def search(
        self,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        location: Optional[str] = None,
        university: Optional[str] = None,
        room_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        try:
            query = {}
            if min_price is not None:
                query["price_per_month"] = {"$gte": min_price}
            if max_price is not None:
                query.setdefault("price_per_month", {})["$lte"] = max_price
            if location:
                query["district_name"] = location
            if university:
                query["university_nearby"] = university
            if room_type:
                query["rental_type"] = room_type

            cursor = self.collection.find(query).skip(skip).limit(limit)
            apartments = []
            async for document in cursor:
                apartments.append(Apartment.from_mongo(document))
            return apartments
        except Exception as e:
            print(e)
            return []

    async def get_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        try:
            pipeline = [
                {
                    "$geoNear": {
                        "near": {"type": "Point", "coordinates": [longitude, latitude]},
                        "distanceField": "distance",
                        "maxDistance": radius_km * 1000,
                        "spherical": True
                    }
                },
                {"$skip": skip},
                {"$limit": limit}
            ]

            cursor = self.collection.aggregate(pipeline)
            apartments = []
            async for document in cursor:
                apartments.append(Apartment.from_mongo(document))
            return apartments
        except Exception as e:
            print(e)
            return []

    async def get_available(
        self,
        check_in: datetime,
        check_out: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        try:
            query = {
                "available_from": {"$lte": check_in},
                "available_until": {"$gte": check_out}
            }

            cursor = self.collection.find(query).skip(skip).limit(limit)
            apartments = []
            async for document in cursor:
                apartments.append(Apartment.from_mongo(document))
            return apartments
        except Exception as e:
            print(e)
            return []

    async def get_promoted(self, skip: int = 0, limit: int = 100) -> List[Apartment]:
        try:
            cursor = self.collection.find({"is_promoted": True}).skip(skip).limit(limit)
            apartments = []
            async for document in cursor:
                apartments.append(Apartment.from_mongo(document))
            return apartments
        except Exception as e:
            print(e)
            return []
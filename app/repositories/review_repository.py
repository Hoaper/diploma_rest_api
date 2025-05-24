from typing import Optional, List
from models.review import Review, ReviewType
from repositories.base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime

class ReviewRepository(BaseRepository[Review]):
    def __init__(self, client: AsyncIOMotorClient):
        self.db = client.get_database("diploma")
        self.collection = self.db["Reviews"]

    async def create(self, entity: Review) -> Review:
        try:
            entity_dict = entity.dict()
            entity_dict["createdAt"] = datetime.utcnow()
            entity_dict["updatedAt"] = datetime.utcnow()
            result = await self.collection.insert_one(entity_dict)
            entity_dict["reviewId"] = str(result.inserted_id)
            return Review(**entity_dict)
        except Exception as e:
            print(e)
            return None

    async def get_by_id(self, entity_id: str) -> Optional[Review]:
        try:
            result = await self.collection.find_one({"_id": ObjectId(entity_id)})
            if result:
                result["reviewId"] = str(result["_id"])
                del result["_id"]
                return Review(**result)
            return None
        except Exception as e:
            print(e)
            return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Review]:
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            reviews = []
            async for document in cursor:
                document["reviewId"] = str(document["_id"])
                del document["_id"]
                reviews.append(Review(**document))
            return reviews
        except Exception as e:
            print(e)
            return []

    async def update(self, entity_id: str, entity: Review) -> Optional[Review]:
        try:
            entity_dict = entity.dict(exclude_unset=True)
            entity_dict["updatedAt"] = datetime.utcnow()
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(entity_id)},
                {"$set": entity_dict},
                return_document=True
            )
            if result:
                result["reviewId"] = str(result["_id"])
                del result["_id"]
                return Review(**result)
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

    async def get_by_target(
        self,
        target_id: str,
        review_type: ReviewType,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        try:
            cursor = self.collection.find({
                "target_id": target_id,
                "review_type": review_type
            }).skip(skip).limit(limit)
            reviews = []
            async for document in cursor:
                document["reviewId"] = str(document["_id"])
                del document["_id"]
                reviews.append(Review(**document))
            return reviews
        except Exception as e:
            print(e)
            return []

    async def get_by_reviewer(
        self,
        reviewer_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        try:
            cursor = self.collection.find({"reviewer_id": reviewer_id}).skip(skip).limit(limit)
            reviews = []
            async for document in cursor:
                document["reviewId"] = str(document["_id"])
                del document["_id"]
                reviews.append(Review(**document))
            return reviews
        except Exception as e:
            print(e)
            return []

    async def get_average_rating(
        self,
        target_id: str,
        review_type: ReviewType
    ) -> float:
        try:
            pipeline = [
                {
                    "$match": {
                        "target_id": target_id,
                        "review_type": review_type
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "average_rating": {"$avg": "$rating"}
                    }
                }
            ]
            
            result = await self.collection.aggregate(pipeline).to_list(length=1)
            if result and result[0]:
                return result[0]["average_rating"]
            return 0.0
        except Exception as e:
            print(e)
            return 0.0

    async def verify_review(self, review_id: str) -> Optional[Review]:
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(review_id)},
                {
                    "$set": {
                        "is_verified": True,
                        "updatedAt": datetime.utcnow()
                    }
                },
                return_document=True
            )
            if result:
                result["reviewId"] = str(result["_id"])
                del result["_id"]
                return Review(**result)
            return None
        except Exception as e:
            print(e)
            return None 
from typing import Optional, List
from datetime import datetime
from models.user import User
from repositories.base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from utils.logging import logger

class UserRepository(BaseRepository[User]):
    def __init__(self, client: AsyncIOMotorClient):
        self.db = client.get_database("diploma")
        self.collection = self.db["User"]

    async def create(self, entity: User) -> User:
        entity_dict = entity.dict(by_alias=True)
        entity_dict["createdAt"] = datetime.utcnow()
        entity_dict["updatedAt"] = datetime.utcnow()
        result = await self.collection.insert_one(entity_dict)
        entity_dict["_id"] = result.inserted_id
        return User.from_mongo(entity_dict)

    async def get_by_id(self, entity_id: str) -> Optional[User]:
        try:
            result = await self.collection.find_one({"_id": ObjectId(entity_id)})
            return User.from_mongo(result) if result else None
        except Exception as e:
            logger.error(f"Error getting user by ID {entity_id}: {str(e)}")
            return None

    async def is_admin(self, user_id: str) -> bool:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user and user.get("admin") is True:
            return True
        return False

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        cursor = self.collection.find().skip(skip).limit(limit)
        users = []
        async for document in cursor:
            users.append(User.from_mongo(document))
        return users

    async def update(self, entity_id: str, entity_data: dict) -> Optional[User]:
        try:
            entity_data["updatedAt"] = datetime.utcnow()
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(entity_id)},
                {"$set": entity_data},
                return_document=True
            )
            return User.from_mongo(result) if result else None
        except Exception as e:
            logger.error(f"Error updating user {entity_id}: {str(e)}")
            return None

    async def delete(self, entity_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(entity_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting user {entity_id}: {str(e)}")
            return False

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.collection.find_one({"email": email})
        return User.from_mongo(result) if result else None

    async def update_last_login(self, user_id: str) -> Optional[User]:
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}},
                return_document=True
            )
            return User.from_mongo(result) if result else None
        except Exception as e:
            logger.error(f"Error updating last login for user {user_id}: {str(e)}")
            return None

    async def get_landlords(self, skip: int = 0, limit: int = 100) -> List[User]:
        cursor = self.collection.find({"is_landlord": True}).skip(skip).limit(limit)
        users = []
        async for document in cursor:
            users.append(User.from_mongo(document))
        return users

    async def verify_landlord(self, user_id: str) -> Optional[User]:
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "is_verified_landlord": True,
                        "updatedAt": datetime.utcnow()
                    }
                },
                return_document=True
            )
            return User.from_mongo(result) if result else None
        except Exception as e:
            logger.error(f"Error verifying landlord {user_id}: {str(e)}")
            return None

    async def get_by_university(self, university: str, skip: int = 0, limit: int = 100) -> List[User]:
        cursor = self.collection.find({"university": university}).skip(skip).limit(limit)
        users = []
        async for document in cursor:
            users.append(User.from_mongo(document))
        return users 
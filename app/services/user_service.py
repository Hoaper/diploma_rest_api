from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from models.user import User
from repositories.user_repository import UserRepository
from fastapi import HTTPException
from services.base import BaseService
from utils.logging import logger

class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, entity_id: str) -> Optional[User]:
        try:
            return await self.user_repository.get_by_id(entity_id)
        except ValueError as e:
            logger.error(f"Error getting user by ID {entity_id}: {str(e)}")
            return None

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[User]:
        return await self.user_repository.get_all(skip, limit)

    async def update(self, entity_id: str, entity_data: dict) -> Optional[User]:
        try:
            entity_data["updatedAt"] = datetime.utcnow()
            return await self.user_repository.update(entity_id, entity_data)
        except ValueError as e:
            logger.error(f"Error updating user {entity_id}: {str(e)}")
            return None

    async def delete(self, entity_id: str) -> bool:
        try:
            return await self.user_repository.delete(entity_id)
        except ValueError as e:
            logger.error(f"Error deleting user {entity_id}: {str(e)}")
            return False

    async def create(self, user: User) -> User:
        user.createdAt = datetime.utcnow()
        user.updatedAt = datetime.utcnow()
        return await self.user_repository.create(user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)

    async def get_landlords(self, skip: int = 0, limit: int = 10) -> List[User]:
        return await self.user_repository.get_landlords(skip, limit)

    async def verify_landlord(self, user_id: str) -> Optional[User]:
        try:
            return await self.user_repository.verify_landlord(user_id)
        except ValueError as e:
            logger.error(f"Error verifying landlord {user_id}: {str(e)}")
            return None

    async def get_users_by_university(self, university: str, skip: int = 0, limit: int = 10) -> List[User]:
        return await self.user_repository.get_by_university(university, skip, limit)

    async def update_last_login(self, user_id: str) -> Optional[User]:
        try:
            return await self.user_repository.update_last_login(user_id)
        except ValueError as e:
            logger.error(f"Error updating last login for user {user_id}: {str(e)}")
            return None

    async def create_user(self, user: User) -> User:
        user.createdAt = datetime.utcnow()
        user.updatedAt = datetime.utcnow()
        return await self.user_repository.create(user)

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        try:
            user_data["updatedAt"] = datetime.utcnow()
            return await self.user_repository.update(user_id, user_data)
        except ValueError as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return None

    async def delete_user(self, user_id: str) -> bool:
        try:
            return await self.user_repository.delete(user_id)
        except ValueError as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            return False

    async def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return await self.user_repository.get_all(skip, limit)

    async def get_by_university(self, university: str) -> List[User]:
        return await self.user_repository.get_by_university(university)

    async def get_user_profile(self, user_id: str) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            logger.error(f"User profile not found for ID {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_user_profile(self, user: User) -> User:
        existing_user = await self.user_repository.get_by_email(user.email)
        if existing_user:
            logger.error(f"User with email {user.email} already exists")
            raise HTTPException(status_code=400, detail="User with this email already exists")
        return await self.user_repository.create(user)

    async def update_user_profile(self, user_id: str, user_data: User) -> User:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            logger.error(f"User profile not found for ID {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return await self.user_repository.update(user_id, user_data) 
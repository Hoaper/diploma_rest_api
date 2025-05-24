from typing import Optional, List
from datetime import datetime
from models.review import Review, ReviewType
from repositories.review_repository import ReviewRepository
from services.base import BaseService
from fastapi import HTTPException

class ReviewService(BaseService[Review]):
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    async def create(self, review: Review) -> Review:
        review.created_at = datetime.utcnow()
        review.updated_at = datetime.utcnow()
        return await self.review_repository.create(review)

    async def get_by_id(self, review_id: str) -> Optional[Review]:
        return await self.review_repository.get_by_id(review_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Review]:
        return await self.review_repository.get_all(skip, limit)

    async def update(self, review_id: str, review: Review) -> Optional[Review]:
        review.updated_at = datetime.utcnow()
        return await self.review_repository.update(review_id, review)

    async def delete(self, review_id: str) -> bool:
        return await self.review_repository.delete(review_id)

    async def get_by_target(
        self,
        target_id: str,
        review_type: ReviewType,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        return await self.review_repository.get_by_target(
            target_id, review_type, skip, limit
        )

    async def get_by_reviewer(
        self,
        reviewer_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        return await self.review_repository.get_by_reviewer(
            reviewer_id, skip, limit
        )

    async def get_average_rating(
        self,
        target_id: str,
        review_type: ReviewType
    ) -> float:
        return await self.review_repository.get_average_rating(
            target_id, review_type
        )

    async def verify_review(self, review_id: str) -> Optional[Review]:
        review = await self.review_repository.get_by_id(review_id)
        if review:
            review.is_verified = True
            review.updated_at = datetime.utcnow()
            return await self.review_repository.update(review_id, review)
        return None

    async def create_review(self, review: Review) -> Review:
        return await self.review_repository.create(review)

    async def get_review(self, review_id: str) -> Review:
        review = await self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    async def update_review(self, review_id: str, review_data: Review) -> Review:
        existing_review = await self.review_repository.get_by_id(review_id)
        if not existing_review:
            raise HTTPException(status_code=404, detail="Review not found")
        return await self.review_repository.update(review_id, review_data)

    async def delete_review(self, review_id: str) -> bool:
        success = await self.review_repository.delete(review_id)
        if not success:
            raise HTTPException(status_code=404, detail="Review not found")
        return True

    async def get_target_reviews(
        self,
        target_id: str,
        review_type: ReviewType,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        return await self.review_repository.get_by_target(
            target_id=target_id,
            review_type=review_type,
            skip=skip,
            limit=limit
        )

    async def get_reviewer_reviews(
        self,
        reviewer_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Review]:
        return await self.review_repository.get_by_reviewer(
            reviewer_id=reviewer_id,
            skip=skip,
            limit=limit
        )

    async def verify_review(self, review_id: str) -> Review:
        review = await self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return await self.review_repository.verify_review(review_id) 
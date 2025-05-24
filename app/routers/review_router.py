from fastapi import APIRouter, Depends, Query
from typing import List
from models.review import Review, ReviewType
from services.review_service import ReviewService
from dependencies import get_review_service

router = APIRouter(prefix="/api/v1", tags=["reviews"])

@router.post("/reviews", response_model=Review)
async def create_review(
    review: Review,
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.create_review(review)

@router.get("/reviews/{review_id}", response_model=Review)
async def get_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_review(review_id)

@router.patch("/reviews/{review_id}", response_model=Review)
async def update_review(
    review_id: str,
    review_data: Review,
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.update_review(review_id, review_data)

@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.delete_review(review_id)

@router.get("/reviews/target/{target_id}", response_model=List[Review])
async def get_target_reviews(
    target_id: str,
    review_type: ReviewType,
    skip: int = Query(0),
    limit: int = Query(100),
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_target_reviews(
        target_id=target_id,
        review_type=review_type,
        skip=skip,
        limit=limit
    )

@router.get("/reviews/reviewer/{reviewer_id}", response_model=List[Review])
async def get_reviewer_reviews(
    reviewer_id: str,
    skip: int = Query(0),
    limit: int = Query(100),
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_reviewer_reviews(
        reviewer_id=reviewer_id,
        skip=skip,
        limit=limit
    )

@router.get("/reviews/average-rating")
async def get_average_rating(
    target_id: str = Query(...),
    review_type: ReviewType = Query(...),
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_average_rating(target_id, review_type)

@router.post("/reviews/{review_id}/verify", response_model=Review)
async def verify_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.verify_review(review_id) 
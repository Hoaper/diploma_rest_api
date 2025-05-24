from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.user import User
from services.user_service import UserService
from dependencies import get_user_service, get_current_user

router = APIRouter(prefix="/api/v1", tags=["users"])

@router.get("/profile", response_model=User)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get user profile information"""
    return current_user

@router.post("/profile", response_model=dict)
async def create_user_profile(
    user: User,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Create or fill user profile"""
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    created_user = await user_service.create(user)
    return {
        "message": "Profile created successfully.",
        "userId": created_user.userId
    }

@router.patch("/profile", response_model=dict)
async def update_user_profile(
    user_data: dict,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update user profile"""
    updated_user = await user_service.update(current_user.userId, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Profile updated successfully."}

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_data: dict,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/", response_model=List[User])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all_users(skip, limit)

@router.get("/landlords", response_model=List[User])
async def get_landlords(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_landlords(skip, limit)

@router.post("/{user_id}/verify-landlord", response_model=User)
async def verify_landlord(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.verify_landlord(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/university/{university}", response_model=List[User])
async def get_users_by_university(
    university: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_users_by_university(university, skip, limit)

@router.post("/{user_id}/last-login")
async def update_last_login(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.update_last_login(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Last login updated successfully"} 
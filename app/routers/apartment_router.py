from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import datetime
from models.apartment import Apartment
from services.apartment_service import ApartmentService
from dependencies import get_apartment_service, get_current_user
from models.user import User
from logging import log

router = APIRouter(prefix="/api/v1", tags=["apartments"])

@router.get("/apartments/search", response_model=List[Apartment])
async def search_apartments(
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    location: Optional[str] = Query(None),
    university: Optional[str] = Query(None),
    room_type: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(100),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    return await apartment_service.search_apartments(
        min_price=min_price,
        max_price=max_price,
        location=location,
        university=university,
        room_type=room_type,
        skip=skip,
        limit=limit
    )

@router.get("/apartments/nearby", response_model=List[Apartment])
async def get_nearby_apartments(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(5.0),
    skip: int = Query(0),
    limit: int = Query(100),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    return await apartment_service.get_nearby_apartments(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        skip=skip,
        limit=limit
    )

@router.get("/apartments/available", response_model=List[Apartment])
async def get_available_apartments(
    check_in: datetime = Query(...),
    check_out: datetime = Query(...),
    skip: int = Query(0),
    limit: int = Query(100),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    return await apartment_service.get_available_apartments(
        check_in=check_in,
        check_out=check_out,
        skip=skip,
        limit=limit
    )

@router.get("/apartments/promoted", response_model=List[Apartment])
async def get_promoted_apartments(
    skip: int = Query(0),
    limit: int = Query(100),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    return await apartment_service.get_promoted_apartments(skip=skip, limit=limit)

@router.get("/apartments/owner/{owner_id}", response_model=List[Apartment])
async def get_owner_apartments(
    owner_id: str,
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    return await apartment_service.get_owner_apartments(owner_id)

@router.post("/apartments", response_model=Apartment)
async def create_apartment(
    apartment: Apartment,
    current_user: User = Depends(get_current_user),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    apartment.ownerId = current_user.userId  # Заменяем ownerId из токена
    return await apartment_service.create_apartment(apartment)

@router.get("/apartments/{apartment_id}", response_model=Apartment)
async def get_apartment(
    apartment_id: str,
    apartment_service: ApartmentService = Depends(get_apartment_service),
    current_user: User = Depends(get_current_user)  # ⬅️ авторизация
):
    return await apartment_service.get_apartment(apartment_id)

@router.patch("/apartments/{apartment_id}", response_model=Apartment)
async def update_apartment(
    apartment_id: str,
    apartment_data: Apartment,
    current_user: User = Depends(get_current_user),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    return await apartment_service.update_apartment(apartment_id, apartment_data, current_user.userId)

@router.delete("/apartments/{apartment_id}")
async def delete_apartment(
    apartment_id: str,
    current_user: User = Depends(get_current_user),
    apartment_service: ApartmentService = Depends(get_apartment_service)
):
    await apartment_service.delete_apartment(apartment_id, current_user.userId)
    return {"message": "Apartment deleted successfully."} 
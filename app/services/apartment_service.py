from typing import Optional, List
from datetime import datetime
from models.apartment import Apartment
from repositories.apartment_repository import ApartmentRepository
from fastapi import HTTPException

class ApartmentService:
    def __init__(self, apartment_repository: ApartmentRepository):
        self.apartment_repository = apartment_repository

    async def create_apartment(self, apartment: Apartment) -> Apartment:
        return await self.apartment_repository.create(apartment)

    async def get_apartment(self, apartment_id: str) -> Apartment:
        apartment = await self.apartment_repository.get_by_id(apartment_id)
        if not apartment:
            raise HTTPException(status_code=404, detail="Apartment not found")
        return apartment

    async def update_apartment(self, apartment_id: str, apartment_data: Apartment, user_id: str) -> Apartment:
        existing_apartment = await self.apartment_repository.get_by_id(apartment_id)
        if not existing_apartment:
            raise HTTPException(status_code=404, detail="Apartment not found")

        if existing_apartment.ownerId != user_id:
            raise HTTPException(status_code=403, detail="You are not the owner of this apartment")

        return await self.apartment_repository.update(apartment_id, apartment_data)

    async def delete_apartment(self, apartment_id: str, user_id: str) -> bool:
        existing_apartment = await self.apartment_repository.get_by_id(apartment_id)
        if not existing_apartment:
            raise HTTPException(status_code=404, detail="Apartment not found")

        if existing_apartment.ownerId != user_id:
            raise HTTPException(status_code=403, detail="You are not the owner of this apartment")

        success = await self.apartment_repository.delete(apartment_id)
        if not success:
            raise HTTPException(status_code=404, detail="Apartment not found")
        return True

    async def get_owner_apartments(self, owner_id: str) -> List[Apartment]:
        return await self.apartment_repository.get_by_owner(owner_id)

    async def search_apartments(
        self,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        location: Optional[str] = None,
        university: Optional[str] = None,
        room_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        return await self.apartment_repository.search(
            min_price=min_price,
            max_price=max_price,
            location=location,
            university=university,
            room_type=room_type,
            skip=skip,
            limit=limit
        )

    async def get_nearby_apartments(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        return await self.apartment_repository.get_nearby(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            skip=skip,
            limit=limit
        )

    async def get_available_apartments(
        self,
        check_in: datetime,
        check_out: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        return await self.apartment_repository.get_available(
            check_in=check_in,
            check_out=check_out,
            skip=skip,
            limit=limit
        )

    async def get_promoted_apartments(self, skip: int = 0, limit: int = 100) -> List[Apartment]:
        return await self.apartment_repository.get_promoted(skip=skip, limit=limit) 
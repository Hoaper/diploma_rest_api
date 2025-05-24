from typing import Optional, List
from datetime import datetime
from models.booking import Booking, BookingStatus
from repositories.booking_repository import BookingRepository
from fastapi import HTTPException


class BookingService:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    async def create_booking(self, booking: Booking) -> Booking:
        is_available = await self.booking_repository.check_availability(
            booking.apartmentId,
            booking.check_in_date,
            booking.check_out_date
        )
        if not is_available:
            raise HTTPException(status_code=400, detail="Apartment is not available for the selected dates")
        return await self.booking_repository.create(booking)

    async def get_booking(self, booking_id: str) -> Booking:
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking

    async def update_booking(self, booking_id: str, booking_data: Booking) -> Booking:
        existing_booking = await self.booking_repository.get_by_id(booking_id)
        if not existing_booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return await self.booking_repository.update(booking_id, booking_data)

    async def delete_booking(self, booking_id: str) -> bool:
        success = await self.booking_repository.delete(booking_id)
        if not success:
            raise HTTPException(status_code=404, detail="Booking not found")
        return True

    async def get_user_bookings(self, user_id: str) -> List[Booking]:
        return await self.booking_repository.get_by_user(user_id)

    async def get_apartment_bookings(self, apartment_id: str) -> List[Booking]:
        return await self.booking_repository.get_by_apartment(apartment_id)

    async def get_bookings_by_status(
        self,
        status: BookingStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Booking]:
        return await self.booking_repository.get_by_status(status, skip, limit)

    async def update_booking_status(
        self,
        booking_id: str,
        status: BookingStatus
    ) -> Booking:
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return await self.booking_repository.update_status(booking_id, status)

    async def check_availability(
        self,
        apartment_id: str,
        check_in: datetime,
        check_out: datetime
    ) -> bool:
        return await self.booking_repository.check_availability(
            apartment_id,
            check_in,
            check_out
        )
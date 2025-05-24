from fastapi import APIRouter, Depends, Query
from typing import List
from datetime import datetime
from models.booking import Booking, BookingStatus
from services.booking_service import BookingService
from dependencies import get_booking_service
from dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/v1", tags=["bookings"])

@router.post("/bookings", response_model=Booking)
async def create_booking(
        booking: Booking,
        booking_service: BookingService = Depends(get_booking_service),
        current_user: User = Depends(get_current_user),
):
    booking.userId = current_user.userId

    return await booking_service.create_booking(booking)

@router.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: str,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.get_booking(booking_id)

@router.patch("/bookings/{booking_id}", response_model=Booking)
async def update_booking(
    booking_id: str,
    booking_data: Booking,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.update_booking(booking_id, booking_data)

@router.delete("/bookings/{booking_id}")
async def delete_booking(
    booking_id: str,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.delete_booking(booking_id)

@router.get("/bookings/user/{user_id}", response_model=List[Booking])
async def get_user_bookings(
    user_id: str,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.get_user_bookings(user_id)

@router.get("/bookings/apartment/{apartment_id}", response_model=List[Booking])
async def get_apartment_bookings(
    apartment_id: str,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.get_apartment_bookings(apartment_id)

@router.get("/bookings/status/{status}", response_model=List[Booking])
async def get_bookings_by_status(
    status: BookingStatus,
    skip: int = Query(0),
    limit: int = Query(100),
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.get_bookings_by_status(status, skip, limit)

@router.patch("/bookings/{booking_id}/status", response_model=Booking)
async def update_booking_status(
    booking_id: str,
    status: BookingStatus,
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.update_booking_status(booking_id, status)

@router.get("/bookings/check-availability")
async def check_availability(
    apartment_id: str = Query(...),
    check_in: datetime = Query(...),
    check_out: datetime = Query(...),
    booking_service: BookingService = Depends(get_booking_service)
):
    return await booking_service.check_availability(apartment_id, check_in, check_out) 
from motor.motor_asyncio import AsyncIOMotorClient
from services.user_service import UserService
from services.apartment_service import ApartmentService
from services.booking_service import BookingService
from services.review_service import ReviewService
from repositories.user_repository import UserRepository
from repositories.apartment_repository import ApartmentRepository
from repositories.booking_repository import BookingRepository
from repositories.review_repository import ReviewRepository
from fastapi import Depends, HTTPException, status, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from models.user import User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# Security scheme for SwaggerUI
security = HTTPBearer()

# MongoDB client
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)

# Repository instances
user_repository = UserRepository(client)
apartment_repository = ApartmentRepository(client)
booking_repository = BookingRepository(client)
review_repository = ReviewRepository(client)

# Service instances
user_service = UserService(user_repository)
apartment_service = ApartmentService(apartment_repository)
booking_service = BookingService(booking_repository)
review_service = ReviewService(review_repository)

# Dependency functions
def get_user_service() -> UserService:
    return user_service

def get_apartment_service() -> ApartmentService:
    return apartment_service

def get_booking_service() -> BookingService:
    return booking_service

def get_review_service() -> ReviewService:
    return review_service



async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Optional[User]:
    if credentials is None:
        return None
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        userId: str = payload.get("userId", None)
        if userId is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_service.get_by_id(userId)
    if user is None:
        raise credentials_exception
    return user

async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user is None or not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only.",
        )
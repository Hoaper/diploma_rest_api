from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from datetime import datetime
from utils.logging import logger

# Load environment variables
load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET environment variable is not set")
ALGORITHM = "HS256"

class TokenData(BaseModel):
    userId: str
    email: str
    name: str
    exp: datetime
    iat: datetime

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[TokenData]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                logger.error("Invalid authentication scheme")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                )
            
            try:
                # Декодируем токен с проверкой подписи и срока действия
                payload = jwt.decode(
                    credentials.credentials,
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                    options={
                        "verify_signature": True,
                        "verify_exp": True,
                        "verify_iat": True,
                        "require": ["exp", "iat", "userId", "email", "name"]
                    }
                )
                
                # Проверяем наличие всех необходимых полей
                userId: str = payload.get("userId")
                email: str = payload.get("email")
                name: str = payload.get("name")
                exp: datetime = payload.get("exp")
                iat: datetime = payload.get("iat")
                
                if any(field is None for field in [userId, email, name, exp, iat]):
                    logger.error("Invalid token payload - missing required fields")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token payload",
                    )
                    
                return TokenData(
                    userId=userId,
                    email=email,
                    name=name,
                    exp=exp,
                    iat=iat
                )
            except jwt.ExpiredSignatureError:
                logger.error("Token has expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                )
            except jwt.InvalidTokenError as e:
                logger.error(f"Invalid token: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token: {str(e)}",
                )
        else:
            logger.error("Invalid authorization code")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code",
            ) 
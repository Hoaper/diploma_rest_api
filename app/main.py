from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_router import router as user_router
from routers.apartment_router import router as apartment_router
from routers.booking_router import router as booking_router
from routers.review_router import router as review_router
from dependencies import security

# Initialize FastAPI app
app = FastAPI(
    title="Student Housing API",
    description="API for student housing application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security scheme to OpenAPI
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True
}


# Include routers
app.include_router(user_router)
app.include_router(apartment_router)
app.include_router(booking_router)
app.include_router(review_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 

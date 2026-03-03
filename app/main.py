from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
import os

# Load environment variables from .env file (if present)
load_dotenv()

from app.api import auth, listings, bids, payments
from app.database import create_db_and_tables

app = FastAPI(
    title="ZimLivestock API",
    description="Backend API for Zimbabwe's Premier Livestock Marketplace",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:3005",
    "http://localhost:3006",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error for {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(bids.router)
app.include_router(payments.router)



@app.get("/")
async def root():
    return {"message": "Welcome to ZimLivestock API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

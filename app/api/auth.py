from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, UserBase
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Union

router = APIRouter(prefix="/auth", tags=["auth"])

# simple mock hashing used for MVP; not secure

# Pydantic schemata for API interaction
class UserCreate(UserBase):
    password: str

    # ensure email is normalized and phone is sensible
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        phone = v.strip()
        if not phone.isdigit() or len(phone) < 7:
            raise ValueError("phone number must contain only digits and be at least 7 characters long")
        return phone

class UserRead(UserBase):
    id: int

class UserLogin(BaseModel):
    contact: Union[EmailStr, str]  # email or phone
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# password helpers (mock implementation)

def hash_password(password: str) -> str:
    # very simple placeholder; DO NOT use in production
    return password + "#zmhash"


def verify_password(plain: str, hashed: str) -> bool:
    return hashed == plain + "#zmhash"

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check for existing account using email *or* phone
    statement = select(User).where(
        (User.email == user.email) | (User.phone == user.phone)
    )
    existing_user = session.exec(statement).first()
    if existing_user:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    # we cannot use from_orm anymore (it expects a password_hash field),
    # so build the model manually from the UserCreate data.
    db_user = User(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        phone=user.phone,
        avatar=user.avatar,
        location=user.location,
        verified=user.verified,
    )
    db_user.password_hash = hash_password(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    # Accept either email or phone as contact
    statement = select(User).where(
        (User.email == credentials.contact) | (User.phone == credentials.contact)
    )
    user = session.exec(statement).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return fake token for now (replace with JWT later)
    return {"access_token": f"fake-jwt-token-for-{user.id}", "token_type": "bearer"}

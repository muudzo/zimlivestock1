from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, UserBase
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

# Pydantic schemata for API interaction
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserLogin(BaseModel):
    contact: str # email or phone
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Mock hashing for now to keep it simple and dependency-free without env setup
def hash_password(password: str) -> str:
    return password + "hashed"

def verify_password(plain: str, hashed: str) -> bool:
    return hashed == plain + "hashed"

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check existing
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User.from_orm(user)
    db_user.password_hash = hash_password(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    # Simple logic: try finding by email
    statement = select(User).where(User.email == credentials.contact)
    user = session.exec(statement).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Return fake token for now
    return {"access_token": f"fake-jwt-token-for-{user.id}", "token_type": "bearer"}

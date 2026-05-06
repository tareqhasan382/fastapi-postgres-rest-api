from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.database import get_db
from app import crud, schemas
import os
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))

def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "type": token_type, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(body: schemas.RegisterRequest, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, body.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, body.email, body.password)

@router.post("/login", response_model=schemas.TokenResponse)
def login(body: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, body.email)
    if not user or not crud.verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")

    access_token = create_token(user.email, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(user.email, "refresh", timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return schemas.TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh(body: schemas.RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = crud.get_user_by_email(db, email)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_token(user.email, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(user.email, "refresh", timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return schemas.TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=schemas.UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user

# @router.get("/me", response_model=schemas.UserResponse)
# def me(db: Session = Depends(get_db), credentials=Depends(__import__('fastapi').security.HTTPBearer())):
#     from app.dependencies import get_current_user
#     # handled via dependency directly in main
#     pass
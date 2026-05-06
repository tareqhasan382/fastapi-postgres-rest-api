from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models import Role

# ── Auth ──────────────────────────────────────────────
class RegisterRequest(BaseModel):
    full_name: Optional[str]
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}

# ── Items ─────────────────────────────────────────────
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}
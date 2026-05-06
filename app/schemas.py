from pydantic import BaseModel
from typing import Optional

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
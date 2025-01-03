from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    address: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

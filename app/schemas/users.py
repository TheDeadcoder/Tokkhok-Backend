from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    userName: str
    email: str

class UserCreate(UserBase):
    id: UUID
    pass

class UserUpdate(BaseModel):
    userName: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

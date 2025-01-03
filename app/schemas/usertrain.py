import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class userTrainBase(BaseModel):
    banglish: str
    bangla: str
    user_id: uuid.UUID

class userTrainCreate(userTrainBase):
    pass

class userTrainUpdate(BaseModel):
    banglish: Optional[str] = None
    bangla: Optional[str] = None
    is_approved: Optional[bool] = None

class userTrainInDBBase(userTrainBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_approved: bool

    class Config:
        orm_mode = True
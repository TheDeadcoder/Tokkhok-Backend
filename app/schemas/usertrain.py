import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class userTrainBase(BaseModel):
    banglish: str
    bangla: str

class userTrainCreate(userTrainBase):
    pass

class userTrainUpdate(userTrainBase):
    banglish: Optional[str] = None
    bangla: Optional[str] = None

class userTrainInDBBase(userTrainBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
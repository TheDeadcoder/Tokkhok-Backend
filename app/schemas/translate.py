import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TranslationBase(BaseModel):
    text: str
    translated_text: str

class TranslationCreate(BaseModel):
    text: Optional[str] = None
    translated_text: Optional[str] = None   
    user_id: uuid.UUID

class TranslationUpdate(BaseModel):
    text: Optional[str] = None
    translated_text: Optional[str] = None

class TranslationInDBBase(TranslationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
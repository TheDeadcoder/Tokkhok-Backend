import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AudioChat(BaseModel):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    query: str
    response: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
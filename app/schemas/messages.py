import uuid
from pydantic import BaseModel, Json
from datetime import datetime
from typing import Dict, List, Optional

class MessageCreate(BaseModel):
    content: str
    
class MessageUpdate(BaseModel):
    content: Optional[str] = None

class Message(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    
    sender: str
    content: str
    knowledge: Optional[List[Dict]] = None
    
    created_at: datetime
    updated_at: datetime
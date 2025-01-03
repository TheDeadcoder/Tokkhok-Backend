import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.messages import Message

class ChatCreate(BaseModel):
    user_id: uuid.UUID
    public_file_ids: Optional[List[uuid.UUID]] = []
    chat_name: str
    
class ChatUpdate(BaseModel):
    chat_name: Optional[str] = None

class Chat(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    
    chat_name: str
    
    created_at: datetime
    updated_at: datetime

class ChatResponse(Chat):
    query: Message
    response: Message
    

class ChatWithMessages(Chat):
    messages: List[Message]
    
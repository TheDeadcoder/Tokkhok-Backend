import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FileCreate(BaseModel):
    uploader_id: uuid.UUID
    status: Optional[str] = 'Completed'
    privacy_status: Optional[str] = 'private'
    text: str

class FileUpdate(BaseModel):
    file_title: Optional[str] = None
    file_caption: Optional[str] = None
    status: Optional[str] = None
    privacy_status: Optional[str] = None

class FileInDBBase(BaseModel):
    id: uuid.UUID
    file_title: str
    file_caption: str
    file_url: str
    uploaded_at: datetime
    uploader_id: uuid.UUID
    status: str
    privacy_status: str


class fileMetadata(BaseModel):
    file_title: str
    file_caption: str
    file_summary: str







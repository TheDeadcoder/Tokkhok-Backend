import uuid
from sqlalchemy import UUID, Column, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    chat_name = Column(String, nullable=False)
    selected_public_file_ids = Column(ARRAY(String), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    user = relationship("User", back_populates="chats")
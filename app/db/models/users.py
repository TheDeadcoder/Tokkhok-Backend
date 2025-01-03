import uuid
from sqlalchemy import Column, String, ARRAY, TIMESTAMP, UUID, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    user_train = relationship("UserTrain", back_populates="user", cascade="all, delete-orphan")

    files = relationship('File', back_populates='uploader')
    translations = relationship('Translation', back_populates='user', cascade='all, delete-orphan')
    audio_chats = relationship("AudioChat", back_populates="user", cascade="all, delete-orphan")
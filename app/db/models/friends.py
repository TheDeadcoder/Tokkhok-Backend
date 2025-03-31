import uuid
from sqlalchemy import Column, String, ARRAY, TIMESTAMP, UUID, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Friend(Base):
    __tablename__ = 'friends'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    friend_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='friends')
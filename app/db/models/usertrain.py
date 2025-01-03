import uuid
from sqlalchemy import Column, String, ARRAY, TIMESTAMP, UUID, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class UserTrain(Base):
    __tablename__ = 'user_train'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    banglish = Column(String, nullable=False)
    bangla = Column(String, nullable=False)

    is_approved = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="user_train")




    
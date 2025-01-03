import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class File(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    file_title = Column(String, nullable=False)
    file_caption = Column(String, nullable=True)

    tags = Column(ARRAY(String), nullable=True)
    image_url = Column(String, nullable=True)

    uploader_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    file_url = Column(String, nullable=False)
    status = Column(String, nullable=True, default='parsing...')
    privacy_status = Column(String, nullable=False, default='private')
    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    uploader = relationship('User', back_populates='files')
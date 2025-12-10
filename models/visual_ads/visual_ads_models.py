from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from db import Base

class VisualAd(Base):
	__tablename__ = "visual_ads"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	med_name = Column(String(255), nullable=False)
	photo_url = Column(Text, nullable=False)  # base64 encoded image
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
	active = Column(Boolean, default=True)

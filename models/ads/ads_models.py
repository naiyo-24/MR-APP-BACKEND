from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base


class Ad(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(Text, nullable=False)  # Base64 encoded image
    heading = Column(String(255), nullable=False)
    tagline = Column(String(255), nullable=True)
    website_link = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

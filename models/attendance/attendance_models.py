from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import Base


class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = Column(Integer, ForeignKey("mr_users.id"), nullable=False, index=True)  # FK to MRUser
    name = Column(String(255), nullable=False)
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    date = Column(Date, nullable=False, index=True)
    check_in_selfie = Column(Text, nullable=True) # Base64 encoded image for check-in
    check_out_selfie = Column(Text, nullable=True)  # Base64 encoded image for check-out
    present = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to MRUser
    user = relationship("MRUser", backref="attendances")

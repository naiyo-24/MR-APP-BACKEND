from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import Base

class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mr_user_id = Column(Integer, ForeignKey("mr_users.id"), nullable=False, index=True)
    doctor_name = Column(String(255), nullable=False)
    phone_no = Column(String(15), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    qualification = Column(String(255), nullable=True)
    specialization = Column(String(255), nullable=True)
    experience = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to chambers
    chambers = relationship("Chamber", back_populates="doctor")

class Chamber(Base):
    __tablename__ = "chambers"

    chamber_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False, index=True)
    chamber_name = Column(String(255), nullable=False)
    chamber_address = Column(String(500), nullable=True)
    chamber_phone_no = Column(String(15), nullable=True)

    doctor = relationship("Doctor", back_populates="chambers")

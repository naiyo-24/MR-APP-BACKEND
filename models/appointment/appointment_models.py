from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import Base

class Appointment(Base):
	__tablename__ = "appointments"

	appointment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	mr_user_id = Column(Integer, ForeignKey("mr_users.id"), nullable=False, index=True)
	doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False, index=True)
	chamber_id = Column(Integer, ForeignKey("chambers.chamber_id"), nullable=False, index=True)
	date = Column(DateTime, nullable=False)
	time = Column(String(20), nullable=False)
	status = Column(String(50), nullable=False, default="scheduled")
	notes = Column(Text, nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

	# Relationships
	mr_user = relationship("MRUser", backref="appointments")
	doctor = relationship("Doctor", backref="appointments")
	chamber = relationship("Chamber", backref="appointments")

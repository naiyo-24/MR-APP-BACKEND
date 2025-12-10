from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from db import Base

class SalarySlip(Base):
	__tablename__ = "salary_slips"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	mr_user_id = Column(Integer, ForeignKey("mr_users.id"), nullable=False, index=True)
	month = Column(String(20), nullable=False)
	year = Column(Integer, nullable=False)
	pdf_base64 = Column(Text, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

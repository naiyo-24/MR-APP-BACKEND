from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from db import Base

class Assignment(Base):
	__tablename__ = "assignments"

	assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	mr_user_id = Column(Integer, ForeignKey("mr_users.id"), nullable=False, index=True)
	headquarter_id = Column(Integer, ForeignKey("headquarters.headquarter_id"), nullable=False, index=True)
	date = Column(DateTime, nullable=False)
	visit_status = Column(String(50), nullable=False, default="pending")
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

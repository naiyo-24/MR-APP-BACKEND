from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from db import Base
import enum


class WorkAreaStatus(str, enum.Enum):
	PENDING = "pending"
	IN_PROGRESS = "in_progress"
	COMPLETED = "completed"


class WorkArea(Base):
	__tablename__ = "work_areas"

	work_area_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	mr_user_id = Column(Integer, ForeignKey("mr_users.id"), nullable=False, index=True)
	under_headquarter = Column(String(255), nullable=True)
	area = Column(String(255), nullable=True)
	date = Column(DateTime(timezone=True), nullable=True)
	status = Column(SQLEnum(WorkAreaStatus), nullable=False, default=WorkAreaStatus.PENDING)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


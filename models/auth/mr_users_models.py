from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from db import Base
import enum


class DesignationType(str, enum.Enum):
    MEDICAL_REPRESENTATIVE = "medical_representative"
    AREA_SALES_MANAGER = "area_sales_manager"
    MARKETING_HEAD = "marketing_head"


class GenderType(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class MRUser(Base):
    __tablename__ = "mr_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    phone_no = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    address = Column(String(500), nullable=True)
    headquarters = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    bank_ac_no = Column(String(20), nullable=True)
    bank_ifsc_code = Column(String(20), nullable=True)
    bank_name = Column(String(255), nullable=True)
    branch_name = Column(String(255), nullable=True)
    upi_id = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(SQLEnum(GenderType), nullable=True)
    profile_photo = Column(Text, nullable=True)  # Base64 encoded image
    alternative_phone_no = Column(String(15), nullable=True)
    designation = Column(SQLEnum(DesignationType), nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

from db import get_db
from models.auth.mr_users_models import MRUser, DesignationType, GenderType

router = APIRouter(prefix="/api/auth/mr-users", tags=["MR Users"])


# Pydantic Enums
class DesignationEnum(str, Enum):
    medical_representative = "medical_representative"
    area_sales_manager = "area_sales_manager"
    marketing_head = "marketing_head"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


# Pydantic Schemas
class MRUserSignup(BaseModel):
    full_name: str
    phone_no: str
    email: EmailStr
    password: str


class MRUserLogin(BaseModel):
    phone_no: str
    password: str


class MRUserResponse(BaseModel):
    id: int
    full_name: str
    phone_no: str
    email: str
    address: Optional[str] = None
    headquarters: Optional[str] = None
    bank_ac_no: Optional[str] = None
    bank_ifsc_code: Optional[str] = None
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    upi_id: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[GenderEnum] = None
    profile_photo: Optional[str] = None  # Base64 encoded image
    alternative_phone_no: Optional[str] = None
    designation: Optional[DesignationEnum] = None
    is_verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class MRUserLoginResponse(BaseModel):
    message: str
    user: MRUserResponse


# Update Schemas
class UpdateFullName(BaseModel):
    full_name: str


class UpdatePhoneNo(BaseModel):
    phone_no: str


class UpdateEmail(BaseModel):
    email: EmailStr


class UpdateAddress(BaseModel):
    address: str


class UpdateHeadquarters(BaseModel):
    headquarters: str


class UpdatePassword(BaseModel):
    password: str


class UpdateBankAcNo(BaseModel):
    bank_ac_no: str


class UpdateBankIfscCode(BaseModel):
    bank_ifsc_code: str


class UpdateBankName(BaseModel):
    bank_name: str


class UpdateBranchName(BaseModel):
    branch_name: str


class UpdateUpiId(BaseModel):
    upi_id: Optional[str] = None


class UpdateDateOfBirth(BaseModel):
    date_of_birth: datetime


class UpdateGender(BaseModel):
    gender: GenderEnum


class UpdateProfilePhoto(BaseModel):
    profile_photo: str  # Base64 encoded image


class UpdateAlternativePhoneNo(BaseModel):
    alternative_phone_no: str


class UpdateDesignation(BaseModel):
    designation: DesignationEnum


class UpdateIsVerified(BaseModel):
    is_verified: bool


class UpdateAllFields(BaseModel):
    full_name: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    headquarters: Optional[str] = None
    password: Optional[str] = None
    bank_ac_no: Optional[str] = None
    bank_ifsc_code: Optional[str] = None
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    upi_id: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[GenderEnum] = None
    profile_photo: Optional[str] = None  # Base64 encoded image
    alternative_phone_no: Optional[str] = None
    designation: Optional[DesignationEnum] = None
    is_verified: Optional[bool] = None


# ==================== AUTH ROUTES ====================

@router.post("/signup", response_model=MRUserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: MRUserSignup, db: Session = Depends(get_db)):
    """Create a new MR User account"""
    # Check if phone number already exists
    existing_phone = db.query(MRUser).filter(MRUser.phone_no == user_data.phone_no).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(MRUser).filter(MRUser.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (password stored as plain text as requested)
    new_user = MRUser(
        full_name=user_data.full_name,
        phone_no=user_data.phone_no,
        email=user_data.email,
        password=user_data.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=MRUserLoginResponse)
def login(login_data: MRUserLogin, db: Session = Depends(get_db)):
    """Login with phone number and password"""
    user = db.query(MRUser).filter(MRUser.phone_no == login_data.phone_no).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    # Plain text password comparison as requested
    if user.password != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    # Update last login
    user.last_login = func.now()
    db.commit()
    db.refresh(user)
    
    return {"message": "Login successful", "user": user}


# ==================== GET ROUTES ====================

@router.get("/", response_model=List[MRUserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all MR Users"""
    users = db.query(MRUser).all()
    return users


@router.get("/{user_id}", response_model=MRUserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get MR User by ID"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ==================== PUT ROUTES (Update each parameter by ID) ====================

@router.put("/{user_id}/full-name", response_model=MRUserResponse)
def update_full_name(user_id: int, data: UpdateFullName, db: Session = Depends(get_db)):
    """Update user's full name"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.full_name = data.full_name
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/phone-no", response_model=MRUserResponse)
def update_phone_no(user_id: int, data: UpdatePhoneNo, db: Session = Depends(get_db)):
    """Update user's phone number"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Check if phone number already exists
    existing = db.query(MRUser).filter(MRUser.phone_no == data.phone_no, MRUser.id != user_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")
    user.phone_no = data.phone_no
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/email", response_model=MRUserResponse)
def update_email(user_id: int, data: UpdateEmail, db: Session = Depends(get_db)):
    """Update user's email"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Check if email already exists
    existing = db.query(MRUser).filter(MRUser.email == data.email, MRUser.id != user_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user.email = data.email
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/address", response_model=MRUserResponse)
def update_address(user_id: int, data: UpdateAddress, db: Session = Depends(get_db)):
    """Update user's address"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.address = data.address
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/headquarters", response_model=MRUserResponse)
def update_headquarters(user_id: int, data: UpdateHeadquarters, db: Session = Depends(get_db)):
    """Update user's headquarters"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.headquarters = data.headquarters
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/password", response_model=MRUserResponse)
def update_password(user_id: int, data: UpdatePassword, db: Session = Depends(get_db)):
    """Update user's password"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.password = data.password
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/bank-ac-no", response_model=MRUserResponse)
def update_bank_ac_no(user_id: int, data: UpdateBankAcNo, db: Session = Depends(get_db)):
    """Update user's bank account number"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.bank_ac_no = data.bank_ac_no
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/bank-ifsc-code", response_model=MRUserResponse)
def update_bank_ifsc_code(user_id: int, data: UpdateBankIfscCode, db: Session = Depends(get_db)):
    """Update user's bank IFSC code"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.bank_ifsc_code = data.bank_ifsc_code
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/bank-name", response_model=MRUserResponse)
def update_bank_name(user_id: int, data: UpdateBankName, db: Session = Depends(get_db)):
    """Update user's bank name"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.bank_name = data.bank_name
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/branch-name", response_model=MRUserResponse)
def update_branch_name(user_id: int, data: UpdateBranchName, db: Session = Depends(get_db)):
    """Update user's branch name"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.branch_name = data.branch_name
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/upi-id", response_model=MRUserResponse)
def update_upi_id(user_id: int, data: UpdateUpiId, db: Session = Depends(get_db)):
    """Update user's UPI ID"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.upi_id = data.upi_id
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/date-of-birth", response_model=MRUserResponse)
def update_date_of_birth(user_id: int, data: UpdateDateOfBirth, db: Session = Depends(get_db)):
    """Update user's date of birth"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.date_of_birth = data.date_of_birth
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/gender", response_model=MRUserResponse)
def update_gender(user_id: int, data: UpdateGender, db: Session = Depends(get_db)):
    """Update user's gender"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.gender = data.gender
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/profile-photo", response_model=MRUserResponse)
def update_profile_photo(user_id: int, data: UpdateProfilePhoto, db: Session = Depends(get_db)):
    """Update user's profile photo (Base64 encoded)"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.profile_photo = data.profile_photo
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/alternative-phone-no", response_model=MRUserResponse)
def update_alternative_phone_no(user_id: int, data: UpdateAlternativePhoneNo, db: Session = Depends(get_db)):
    """Update user's alternative phone number"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.alternative_phone_no = data.alternative_phone_no
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/designation", response_model=MRUserResponse)
def update_designation(user_id: int, data: UpdateDesignation, db: Session = Depends(get_db)):
    """Update user's designation"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.designation = data.designation
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/is-verified", response_model=MRUserResponse)
def update_is_verified(user_id: int, data: UpdateIsVerified, db: Session = Depends(get_db)):
    """Update user's verification status"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_verified = data.is_verified
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=MRUserResponse)
def update_user(user_id: int, data: UpdateAllFields, db: Session = Depends(get_db)):
    """Update multiple user fields at once"""
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Check for unique constraints
    if "phone_no" in update_data:
        existing = db.query(MRUser).filter(MRUser.phone_no == update_data["phone_no"], MRUser.id != user_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")
    
    if "email" in update_data:
        existing = db.query(MRUser).filter(MRUser.email == update_data["email"], MRUser.id != user_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

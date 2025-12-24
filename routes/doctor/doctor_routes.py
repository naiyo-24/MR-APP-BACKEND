from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from db import get_db
from models.doctor.doctor_models import Doctor, Chamber
from models.auth.mr_users_models import MRUser

router = APIRouter(prefix="/api/doctor", tags=["Doctor"])

# Pydantic Schemas
class ChamberSchema(BaseModel):
    chamber_id: Optional[int]
    chamber_name: str
    chamber_address: Optional[str] = None
    chamber_phone_no: Optional[str] = None

    class Config:
        from_attributes = True

class DoctorCreate(BaseModel):
    mr_user_id: int
    doctor_name: str
    phone_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[str] = None
    chambers: List[ChamberSchema] = []

class DoctorResponse(BaseModel):
    doctor_id: int
    mr_user_id: int
    mr_user_full_name: Optional[str] = None
    doctor_name: str
    phone_no: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    chambers: List[ChamberSchema] = []

    class Config:
        from_attributes = True

class DoctorUpdate(BaseModel):
    doctor_name: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[str] = None
    chambers: Optional[List[ChamberSchema]] = None

# ==================== POST ROUTES ====================
@router.post("/mr-user/{mr_user_id}", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(mr_user_id: int, doctor_data: DoctorCreate, db: Session = Depends(get_db)):
    """Add a doctor by MR user ID"""
    # Verify MR user exists
    user = db.query(MRUser).filter(MRUser.id == mr_user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MR User not found")
    
    new_doctor = Doctor(
        mr_user_id=mr_user_id,
        doctor_name=doctor_data.doctor_name,
        phone_no=doctor_data.phone_no,
        email=doctor_data.email,
        address=doctor_data.address,
        qualification=doctor_data.qualification,
        specialization=doctor_data.specialization,
        experience=doctor_data.experience
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    # Add chambers
    for chamber in doctor_data.chambers:
        new_chamber = Chamber(
            doctor_id=new_doctor.doctor_id,
            chamber_name=chamber.chamber_name,
            chamber_address=chamber.chamber_address,
            chamber_phone_no=chamber.chamber_phone_no
        )
        db.add(new_chamber)
    db.commit()
    db.refresh(new_doctor)
    # Fetch chambers
    chambers = db.query(Chamber).filter(Chamber.doctor_id == new_doctor.doctor_id).all()
    return DoctorResponse(**new_doctor.__dict__, chambers=chambers)

# ==================== GET ROUTES ====================
@router.get("/mr-user/{mr_user_id}", response_model=List[DoctorResponse])
def get_doctors_by_mr_user(mr_user_id: int, db: Session = Depends(get_db)):
    """Get all doctors added by MR user ID"""
    # Fetch MR user once (all doctors here belong to this MR user)
    user = db.query(MRUser).filter(MRUser.id == mr_user_id).first()
    full_name = user.full_name if user else None

    doctors = db.query(Doctor).filter(Doctor.mr_user_id == mr_user_id).all()
    responses = []
    for doctor in doctors:
        chambers = db.query(Chamber).filter(Chamber.doctor_id == doctor.doctor_id).all()
        responses.append(DoctorResponse(**doctor.__dict__, chambers=chambers, mr_user_full_name=full_name))
    return responses

@router.get("/", response_model=List[DoctorResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    """Get all doctors"""
    doctors = db.query(Doctor).all()
    responses = []
    for doctor in doctors:
        chambers = db.query(Chamber).filter(Chamber.doctor_id == doctor.doctor_id).all()
        # Fetch MR user full name for each doctor
        user = db.query(MRUser).filter(MRUser.id == doctor.mr_user_id).first()
        full_name = user.full_name if user else None
        responses.append(DoctorResponse(**doctor.__dict__, chambers=chambers, mr_user_full_name=full_name))
    return responses

# ==================== PUT ROUTES ====================
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_data: DoctorUpdate, db: Session = Depends(get_db)):
    """Update doctor details by doctor ID"""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    update_data = doctor_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key != "chambers":
            setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    # Update chambers if provided
    if "chambers" in update_data and update_data["chambers"] is not None:
        # Delete existing chambers
        db.query(Chamber).filter(Chamber.doctor_id == doctor_id).delete()
        db.commit()
        # Add new chambers
        for chamber in update_data["chambers"]:
            new_chamber = Chamber(
                doctor_id=doctor_id,
                chamber_name=chamber.chamber_name,
                chamber_address=chamber.chamber_address,
                chamber_phone_no=chamber.chamber_phone_no
            )
            db.add(new_chamber)
        db.commit()
    chambers = db.query(Chamber).filter(Chamber.doctor_id == doctor_id).all()
    return DoctorResponse(**doctor.__dict__, chambers=chambers)


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db import get_db
from models.appointment.appointment_models import Appointment
from models.auth.mr_users_models import MRUser
from models.doctor.doctor_models import Doctor, Chamber

router = APIRouter(prefix="/api/appointment", tags=["Appointment"])

# Pydantic Schemas
class AppointmentCreate(BaseModel):
	mr_user_id: int
	doctor_id: int
	chamber_id: int
	date: datetime
	time: str
	status: Optional[str] = "scheduled"
	notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
	date: Optional[datetime] = None
	time: Optional[str] = None
	status: Optional[str] = None
	notes: Optional[str] = None
	chamber_id: Optional[int] = None

class AppointmentResponse(BaseModel):
	appointment_id: int
	mr_user_id: int
	doctor_id: int
	chamber_id: int
	date: datetime
	time: str
	status: str
	notes: Optional[str] = None
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None

	class Config:
		from_attributes = True

# POST: Create appointment
@router.post("/mr-user/{mr_user_id}", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(mr_user_id: int, data: AppointmentCreate, db: Session = Depends(get_db)):
	# Verify MR user, doctor, chamber exist
	user = db.query(MRUser).filter(MRUser.id == mr_user_id).first()
	doctor = db.query(Doctor).filter(Doctor.doctor_id == data.doctor_id).first()
	chamber = db.query(Chamber).filter(Chamber.chamber_id == data.chamber_id).first()
	if not user:
		raise HTTPException(status_code=404, detail="MR User not found")
	if not doctor:
		raise HTTPException(status_code=404, detail="Doctor not found")
	if not chamber:
		raise HTTPException(status_code=404, detail="Chamber not found")
	appointment = Appointment(
		mr_user_id=mr_user_id,
		doctor_id=data.doctor_id,
		chamber_id=data.chamber_id,
		date=data.date,
		time=data.time,
		status=data.status,
		notes=data.notes
	)
	db.add(appointment)
	db.commit()
	db.refresh(appointment)
	return appointment


# Extended response schema
class DoctorInfo(BaseModel):
	doctor_id: int
	doctor_name: str
	phone_no: Optional[str] = None
	email: Optional[str] = None
	address: Optional[str] = None
	qualification: Optional[str] = None
	specialization: Optional[str] = None
	experience: Optional[str] = None

	class Config:
		from_attributes = True

class ChamberInfo(BaseModel):
	chamber_id: int
	chamber_name: str
	chamber_address: Optional[str] = None
	chamber_phone_no: Optional[str] = None

	class Config:
		from_attributes = True

class MRUserInfo(BaseModel):
	id: int
	full_name: str

	class Config:
		from_attributes = True


class AppointmentFullResponse(AppointmentResponse):
	mr_user_full_name: str
	doctor: DoctorInfo
	chamber: ChamberInfo

# GET: Get appointments by MR user ID (with doctor and chamber details)
@router.get("/mr-user/{mr_user_id}", response_model=List[AppointmentFullResponse])
def get_appointments_by_mr_user(mr_user_id: int, db: Session = Depends(get_db)):
	user = db.query(MRUser).filter(MRUser.id == mr_user_id).first()
	if not user:
		raise HTTPException(status_code=404, detail="MR User not found")

	appointments = db.query(Appointment).filter(Appointment.mr_user_id == mr_user_id).all()
	results = []
	for appt in appointments:
		doctor = db.query(Doctor).filter(Doctor.doctor_id == appt.doctor_id).first()
		chamber = db.query(Chamber).filter(Chamber.chamber_id == appt.chamber_id).first()
		doctor_info = DoctorInfo(**doctor.__dict__) if doctor else None
		chamber_info = ChamberInfo(**chamber.__dict__) if chamber else None
		results.append(AppointmentFullResponse(
			**appt.__dict__,
			mr_user_full_name=user.full_name,
			doctor=doctor_info,
			chamber=chamber_info
		))
	return results

# PUT: Update appointment by appointment ID (only if belongs to MR user)
@router.put("/mr-user/{mr_user_id}/appointment/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(mr_user_id: int, appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db)):
	appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id, Appointment.mr_user_id == mr_user_id).first()
	if not appointment:
		raise HTTPException(status_code=404, detail="Appointment not found for this MR user")
	update_data = data.model_dump(exclude_unset=True)
	for key, value in update_data.items():
		setattr(appointment, key, value)
	db.commit()
	db.refresh(appointment)
	return appointment

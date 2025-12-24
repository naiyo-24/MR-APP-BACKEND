from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

from db import get_db
from models.attendance.attendance_models import Attendance
from models.auth.mr_users_models import MRUser

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


# Pydantic Schemas
class AttendanceCreate(BaseModel):
    id: int  # MR User ID (FK)
    name: str
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    date: date
    selfie_proof: Optional[str] = None  # Base64 encoded image
    present: bool = False


class AttendanceResponse(BaseModel):
    attendance_id: int
    id: int  # MR User ID (FK)
    name: str
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    date: date
    selfie_proof: Optional[str] = None  # Base64 encoded image
    present: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Update Schemas
class UpdateCheckInTime(BaseModel):
    check_in_time: datetime


class UpdateCheckOutTime(BaseModel):
    check_out_time: datetime


class UpdateSelfieProof(BaseModel):
    selfie_proof: str  # Base64 encoded image


class UpdatePresent(BaseModel):
    present: bool


class UpdateAttendance(BaseModel):
    name: Optional[str] = None
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    date: Optional[date] = None
    selfie_proof: Optional[str] = None
    present: Optional[bool] = None


# ==================== POST ROUTES ====================

# POST: Create a new attendance record for an MR user
@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(attendance_data: AttendanceCreate, db: Session = Depends(get_db)):
    """Create a new attendance record"""
    # Verify user exists
    user = db.query(MRUser).filter(MRUser.id == attendance_data.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MR User not found"
        )
    
    # Check if attendance already exists for this user on this date
    existing_attendance = db.query(Attendance).filter(
        Attendance.id == attendance_data.id,
        Attendance.date == attendance_data.date
    ).first()
    
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this user on this date"
        )
    
    new_attendance = Attendance(
        id=attendance_data.id,
        name=attendance_data.name,
        check_in_time=attendance_data.check_in_time,
        check_out_time=attendance_data.check_out_time,
        date=attendance_data.date,
        selfie_proof=attendance_data.selfie_proof,
        present=attendance_data.present
    )
    
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    
    return new_attendance


# ==================== GET ROUTES ====================

# GET: Retrieve all attendance records
@router.get("/", response_model=List[AttendanceResponse])
def get_all_attendance(db: Session = Depends(get_db)):
    """Get all attendance records"""
    attendance_records = db.query(Attendance).all()
    return attendance_records


# GET: Retrieve a single attendance record by its ID
@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_by_id(attendance_id: int, db: Session = Depends(get_db)):
    """Get attendance record by attendance ID"""
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    return attendance


# GET: Retrieve all attendance records for a specific MR user
@router.get("/user/{user_id}", response_model=List[AttendanceResponse])
def get_attendance_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Get all attendance records for a specific MR User"""
    # Verify user exists
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MR User not found"
        )
    
    attendance_records = db.query(Attendance).filter(Attendance.id == user_id).all()
    return attendance_records


# GET: Retrieve attendance for a specific MR user on a specific date
@router.get("/user/{user_id}/date/{date}", response_model=AttendanceResponse)
def get_attendance_by_user_and_date(user_id: int, date: date, db: Session = Depends(get_db)):
    """Get attendance record for a specific user on a specific date"""
    attendance = db.query(Attendance).filter(
        Attendance.id == user_id,
        Attendance.date == date
    ).first()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found for this user on this date"
        )
    return attendance


# ==================== PUT ROUTES ====================

# PUT: Update check-in time for an attendance record
@router.put("/{attendance_id}/check-in-time", response_model=AttendanceResponse)
def update_check_in_time(attendance_id: int, data: UpdateCheckInTime, db: Session = Depends(get_db)):
    """Update check-in time"""
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    attendance.check_in_time = data.check_in_time
    db.commit()
    db.refresh(attendance)
    return attendance


# PUT: Update check-out time for an attendance record
@router.put("/{attendance_id}/check-out-time", response_model=AttendanceResponse)
def update_check_out_time(attendance_id: int, data: UpdateCheckOutTime, db: Session = Depends(get_db)):
    """Update check-out time"""
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    attendance.check_out_time = data.check_out_time
    db.commit()
    db.refresh(attendance)
    return attendance


# PUT: Update selfie proof (Base64) for an attendance record
@router.put("/{attendance_id}/selfie-proof", response_model=AttendanceResponse)
def update_selfie_proof(attendance_id: int, data: UpdateSelfieProof, db: Session = Depends(get_db)):
    """Update selfie proof (Base64 encoded image)"""
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    attendance.selfie_proof = data.selfie_proof
    db.commit()
    db.refresh(attendance)
    return attendance


# PUT: Update present/absent status for an attendance record by ID
@router.put("/{attendance_id}/present", response_model=AttendanceResponse)
def update_present_status(attendance_id: int, data: UpdatePresent, db: Session = Depends(get_db)):
    """Update present status"""
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    attendance.present = data.present
    db.commit()
    db.refresh(attendance)
    return attendance


# PUT (admin): Set present/absent for an MR user on a specific date (creates if missing)
@router.put("/admin/user/{user_id}/date/{date}/present", response_model=AttendanceResponse)
def admin_update_present_by_user_and_date(user_id: int, date: date, data: UpdatePresent, db: Session = Depends(get_db)):
    """Admin: set present/absent for a MR user on a specific date. Creates record if missing."""
    # Verify user exists
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MR User not found")

    attendance = db.query(Attendance).filter(Attendance.id == user_id, Attendance.date == date).first()
    if attendance:
        attendance.present = data.present
        attendance.name = user.full_name
    else:
        attendance = Attendance(
            id=user_id,
            name=user.full_name,
            date=date,
            present=data.present
        )
        db.add(attendance)

    db.commit()
    db.refresh(attendance)
    return attendance


# PUT: Update multiple fields of an attendance record
@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, data: UpdateAttendance, db: Session = Depends(get_db)):
    """Update multiple attendance fields at once"""
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(attendance, key, value)
    
    db.commit()
    db.refresh(attendance)
    return attendance


# ==================== ATTENDANCE SUMMARY ROUTES ====================

class MonthlyAttendanceSummary(BaseModel):
    user_id: int
    user_name: str
    year: int
    month: int
    total_days: int
    present_days: int
    absent_days: int
    attendance_percentage: float


# GET: Monthly attendance summary (present/absent counts and percentage) for a user
@router.get("/summary/user/{user_id}/month/{year}/{month}", response_model=MonthlyAttendanceSummary)
def get_monthly_attendance_summary(user_id: int, year: int, month: int, db: Session = Depends(get_db)):
    """Get attendance summary (present/absent days count) for a user in a specific month"""
    import calendar
    
    # Verify user exists
    user = db.query(MRUser).filter(MRUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MR User not found"
        )
    
    # Validate month
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid month. Must be between 1 and 12"
        )
    
    # Get total days in the month
    total_days_in_month = calendar.monthrange(year, month)[1]
    
    # Get start and end date of the month
    start_date = date(year, month, 1)
    end_date = date(year, month, total_days_in_month)
    
    # Query attendance records for the user in the given month
    attendance_records = db.query(Attendance).filter(
        Attendance.id == user_id,
        Attendance.date >= start_date,
        Attendance.date <= end_date
    ).all()
    
    # Count present and absent days
    present_days = sum(1 for record in attendance_records if record.present)
    absent_days = sum(1 for record in attendance_records if not record.present)
    
    # Calculate attendance percentage
    attendance_percentage = (present_days / total_days_in_month) * 100 if total_days_in_month > 0 else 0
    
    return MonthlyAttendanceSummary(
        user_id=user_id,
        user_name=user.full_name,
        year=year,
        month=month,
        total_days=total_days_in_month,
        present_days=present_days,
        absent_days=absent_days,
        attendance_percentage=round(attendance_percentage, 2)
    )

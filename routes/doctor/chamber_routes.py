from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from db import get_db
from models.doctor.chamber_models import Chamber

router = APIRouter(prefix="/api/chamber", tags=["Chamber"])

class ChamberCreate(BaseModel):
    doctor_id: int
    chamber_name: str
    chamber_address: Optional[str] = None
    chamber_phone_no: Optional[str] = None

class ChamberResponse(BaseModel):
    chamber_id: int
    doctor_id: int
    chamber_name: str
    chamber_address: Optional[str] = None
    chamber_phone_no: Optional[str] = None
    class Config:
        from_attributes = True

class ChamberUpdate(BaseModel):
    chamber_name: Optional[str] = None
    chamber_address: Optional[str] = None
    chamber_phone_no: Optional[str] = None

# POST: Add chamber
@router.post("/", response_model=ChamberResponse, status_code=status.HTTP_201_CREATED)
def add_chamber(chamber_data: ChamberCreate, db: Session = Depends(get_db)):
    new_chamber = Chamber(**chamber_data.model_dump())
    db.add(new_chamber)
    db.commit()
    db.refresh(new_chamber)
    return new_chamber

# GET: Get all chambers
@router.get("/", response_model=List[ChamberResponse])
def get_all_chambers(db: Session = Depends(get_db)):
    chambers = db.query(Chamber).all()
    return chambers

# GET: Get chambers by doctor id
@router.get("/doctor/{doctor_id}", response_model=List[ChamberResponse])
def get_chambers_by_doctor(doctor_id: int, db: Session = Depends(get_db)):
    chambers = db.query(Chamber).filter(Chamber.doctor_id == doctor_id).all()
    return chambers

# PUT: Update chamber by chamber id
@router.put("/{chamber_id}", response_model=ChamberResponse)
def update_chamber(chamber_id: int, chamber_data: ChamberUpdate, db: Session = Depends(get_db)):
    chamber = db.query(Chamber).filter(Chamber.chamber_id == chamber_id).first()
    if not chamber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chamber not found")
    update_data = chamber_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(chamber, key, value)
    db.commit()
    db.refresh(chamber)
    return chamber

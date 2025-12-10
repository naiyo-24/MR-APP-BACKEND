from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from db import get_db
from models.headquarter.headquarter_models import Headquarter

router = APIRouter(prefix="/api/headquarters", tags=["Headquarters"])

class HeadquarterCreate(BaseModel):
	name: str
	address: Optional[str] = None
	area_sales_manager_name: str
	contact_no: Optional[str] = None

class HeadquarterUpdate(BaseModel):
	name: Optional[str] = None
	address: Optional[str] = None
	area_sales_manager_name: Optional[str] = None
	contact_no: Optional[str] = None

class HeadquarterResponse(BaseModel):
	headquarter_id: int
	name: str
	address: Optional[str] = None
	area_sales_manager_name: str
	contact_no: Optional[str] = None

	class Config:
		from_attributes = True

# POST
@router.post("/", response_model=HeadquarterResponse, status_code=status.HTTP_201_CREATED)
def create_headquarter(data: HeadquarterCreate, db: Session = Depends(get_db)):
	hq = Headquarter(**data.model_dump())
	db.add(hq)
	db.commit()
	db.refresh(hq)
	return hq

# GET all
@router.get("/", response_model=List[HeadquarterResponse])
def get_all_headquarters(db: Session = Depends(get_db)):
	return db.query(Headquarter).all()

# GET by id
@router.get("/{headquarter_id}", response_model=HeadquarterResponse)
def get_headquarter(headquarter_id: int, db: Session = Depends(get_db)):
	hq = db.query(Headquarter).filter(Headquarter.headquarter_id == headquarter_id).first()
	if not hq:
		raise HTTPException(status_code=404, detail="Headquarter not found")
	return hq

# PUT
@router.put("/{headquarter_id}", response_model=HeadquarterResponse)
def update_headquarter(headquarter_id: int, data: HeadquarterUpdate, db: Session = Depends(get_db)):
	hq = db.query(Headquarter).filter(Headquarter.headquarter_id == headquarter_id).first()
	if not hq:
		raise HTTPException(status_code=404, detail="Headquarter not found")
	update_data = data.model_dump(exclude_unset=True)
	for key, value in update_data.items():
		setattr(hq, key, value)
	db.commit()
	db.refresh(hq)
	return hq

# DELETE
@router.delete("/{headquarter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_headquarter(headquarter_id: int, db: Session = Depends(get_db)):
	hq = db.query(Headquarter).filter(Headquarter.headquarter_id == headquarter_id).first()
	if not hq:
		raise HTTPException(status_code=404, detail="Headquarter not found")
	db.delete(hq)
	db.commit()

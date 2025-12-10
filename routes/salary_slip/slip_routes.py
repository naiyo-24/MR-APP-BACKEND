from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from db import get_db
from models.salary_slip.slip_models import SalarySlip
from models.auth.mr_users_models import MRUser

router = APIRouter(prefix="/api/salary-slip", tags=["Salary Slip"])

class SalarySlipCreate(BaseModel):
	mr_user_id: int
	month: str
	year: int
	pdf_base64: str

class SalarySlipUpdate(BaseModel):
	month: Optional[str] = None
	year: Optional[int] = None
	pdf_base64: Optional[str] = None

class SalarySlipResponse(BaseModel):
	id: int
	mr_user_id: int
	month: str
	year: int
	pdf_base64: str
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None

# POST: Create salary slip
@router.post("/", response_model=SalarySlipResponse, status_code=status.HTTP_201_CREATED)
def create_salary_slip(data: SalarySlipCreate, db: Session = Depends(get_db)):
	user = db.query(MRUser).filter(MRUser.id == data.mr_user_id).first()
	if not user:
		raise HTTPException(status_code=404, detail="MR User not found")
	slip = SalarySlip(**data.model_dump())
	db.add(slip)
	db.commit()
	db.refresh(slip)
	return slip

# GET: Get all salary slips
@router.get("/", response_model=List[SalarySlipResponse])
def get_all_salary_slips(db: Session = Depends(get_db)):
	return db.query(SalarySlip).all()

# GET: Get salary slips by MR user ID
@router.get("/mr-user/{mr_user_id}", response_model=List[SalarySlipResponse])
def get_salary_slips_by_mr_user(mr_user_id: int, db: Session = Depends(get_db)):
	return db.query(SalarySlip).filter(SalarySlip.mr_user_id == mr_user_id).all()

# PUT: Update salary slip by ID
@router.put("/{slip_id}", response_model=SalarySlipResponse)
def update_salary_slip(slip_id: int, data: SalarySlipUpdate, db: Session = Depends(get_db)):
	slip = db.query(SalarySlip).filter(SalarySlip.id == slip_id).first()
	if not slip:
		raise HTTPException(status_code=404, detail="Salary slip not found")
	update_data = data.model_dump(exclude_unset=True)
	for key, value in update_data.items():
		setattr(slip, key, value)
	db.commit()
	db.refresh(slip)
	return slip

# DELETE: Delete salary slip by ID
@router.delete("/{slip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_salary_slip(slip_id: int, db: Session = Depends(get_db)):
	slip = db.query(SalarySlip).filter(SalarySlip.id == slip_id).first()
	if not slip:
		raise HTTPException(status_code=404, detail="Salary slip not found")
	db.delete(slip)
	db.commit()

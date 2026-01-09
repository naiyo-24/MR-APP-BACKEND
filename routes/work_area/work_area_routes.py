from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db import get_db
from models.work_area.work_area_models import WorkArea, WorkAreaStatus
from models.auth.mr_users_models import MRUser

router = APIRouter(prefix="/api/work-area", tags=["Work Area"])


# Pydantic Schemas
class WorkAreaCreate(BaseModel):
	mr_user_id: int
	under_headquarter: Optional[str] = None
	area: Optional[str] = None
	date: Optional[datetime] = None
	status: WorkAreaStatus = WorkAreaStatus.PENDING


class WorkAreaResponse(BaseModel):
	work_area_id: int
	mr_user_id: int
	mr_user_full_name: Optional[str] = None
	under_headquarter: Optional[str] = None
	area: Optional[str] = None
	date: Optional[datetime] = None
	status: WorkAreaStatus
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None

	class Config:
		from_attributes = True


class WorkAreaUpdate(BaseModel):
	mr_user_id: Optional[int] = None
	under_headquarter: Optional[str] = None
	area: Optional[str] = None
	date: Optional[datetime] = None
	status: Optional[WorkAreaStatus] = None


class StatusUpdate(BaseModel):
	status: WorkAreaStatus


# ==================== POST ====================
@router.post("/create", response_model=WorkAreaResponse, status_code=status.HTTP_201_CREATED)
def create_work_area(payload: WorkAreaCreate, db: Session = Depends(get_db)):
	# Verify MR user exists
	user = db.query(MRUser).filter(MRUser.id == payload.mr_user_id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MR User not found")

	work_area = WorkArea(
		mr_user_id=payload.mr_user_id,
		under_headquarter=payload.under_headquarter,
		area=payload.area,
		date=payload.date,
		status=payload.status,
	)
	db.add(work_area)
	db.commit()
	db.refresh(work_area)

	return WorkAreaResponse(**work_area.__dict__, mr_user_full_name=user.full_name)


# ==================== GET ALL ====================
@router.get("/get-all", response_model=List[WorkAreaResponse])
def get_all_work_areas(db: Session = Depends(get_db)):
	items = db.query(WorkArea).all()
	responses = []
	for item in items:
		user = db.query(MRUser).filter(MRUser.id == item.mr_user_id).first()
		full_name = user.full_name if user else None
		responses.append(WorkAreaResponse(**item.__dict__, mr_user_full_name=full_name))
	return responses


# ==================== GET BY WORK ID ====================
@router.get("/get-by/{work_area_id}", response_model=WorkAreaResponse)
def get_work_area_by_id(work_area_id: int, db: Session = Depends(get_db)):
	item = db.query(WorkArea).filter(WorkArea.work_area_id == work_area_id).first()
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work Area not found")
	user = db.query(MRUser).filter(MRUser.id == item.mr_user_id).first()
	full_name = user.full_name if user else None
	return WorkAreaResponse(**item.__dict__, mr_user_full_name=full_name)


# ==================== GET BY MR USER ID ====================
@router.get("/get-by/mr-user/{mr_user_id}", response_model=List[WorkAreaResponse])
def get_work_areas_by_mr_user(mr_user_id: int, db: Session = Depends(get_db)):
	items = db.query(WorkArea).filter(WorkArea.mr_user_id == mr_user_id).all()
	user = db.query(MRUser).filter(MRUser.id == mr_user_id).first()
	full_name = user.full_name if user else None
	return [WorkAreaResponse(**item.__dict__, mr_user_full_name=full_name) for item in items]


# ==================== PUT (UPDATE) BY WORK ID ====================
@router.put("/update-by/{work_area_id}", response_model=WorkAreaResponse)
def update_work_area(work_area_id: int, payload: WorkAreaUpdate, db: Session = Depends(get_db)):
	item = db.query(WorkArea).filter(WorkArea.work_area_id == work_area_id).first()
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work Area not found")

	update_data = payload.model_dump(exclude_unset=True)

	# If mr_user_id is changing, validate
	if "mr_user_id" in update_data and update_data["mr_user_id"] is not None:
		user = db.query(MRUser).filter(MRUser.id == update_data["mr_user_id"]).first()
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MR User not found")
		item.mr_user_id = update_data["mr_user_id"]

	for key in ["under_headquarter", "area", "date", "status"]:
		if key in update_data and update_data[key] is not None:
			setattr(item, key, update_data[key])

	db.commit()
	db.refresh(item)

	user = db.query(MRUser).filter(MRUser.id == item.mr_user_id).first()
	full_name = user.full_name if user else None
	return WorkAreaResponse(**item.__dict__, mr_user_full_name=full_name)


# ==================== PUT UPDATE STATUS BY MR USER ID ====================
@router.put("/update-status/mr-user/{mr_user_id}", response_model=List[WorkAreaResponse])
def update_work_area_status_by_mr_user(mr_user_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
	items = db.query(WorkArea).filter(WorkArea.mr_user_id == mr_user_id).all()
	if not items:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No work areas found for this MR user")
	
	user = db.query(MRUser).filter(MRUser.id == mr_user_id).first()
	full_name = user.full_name if user else None
	
	# Update status for all work areas of this MR user
	for item in items:
		item.status = payload.status
		db.commit()
		db.refresh(item)
	
	return [WorkAreaResponse(**item.__dict__, mr_user_full_name=full_name) for item in items]


# ==================== DELETE BY ID ====================
@router.delete("/delete-by/{work_area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_area(work_area_id: int, db: Session = Depends(get_db)):
	item = db.query(WorkArea).filter(WorkArea.work_area_id == work_area_id).first()
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work Area not found")
	db.delete(item)
	db.commit()
	return None


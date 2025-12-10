from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from db import get_db
from models.visual_ads.visual_ads_models import VisualAd

router = APIRouter(prefix="/api/visual-ads", tags=["Visual Ads"])

class VisualAdCreate(BaseModel):
	med_name: str
	photo_url: str  # base64 encoded image
	active: Optional[bool] = True

class VisualAdResponse(BaseModel):
	id: int
	med_name: str
	photo_url: str
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None
	active: bool


# POST: Create visual ad
@router.post("/", response_model=VisualAdResponse, status_code=status.HTTP_201_CREATED)
def create_visual_ad(data: VisualAdCreate, db: Session = Depends(get_db)):
	ad = VisualAd(**data.model_dump())
	db.add(ad)
	db.commit()
	db.refresh(ad)
	return ad

# GET: Get visual ad by ID
@router.get("/{ad_id}", response_model=VisualAdResponse)
def get_visual_ad(ad_id: int, db: Session = Depends(get_db)):
	ad = db.query(VisualAd).filter(VisualAd.id == ad_id).first()
	if not ad:
		raise HTTPException(status_code=404, detail="Visual Ad not found")
	return ad

# GET: List all visual ads
@router.get("/", response_model=List[VisualAdResponse])
def get_all_visual_ads(db: Session = Depends(get_db)):
	return db.query(VisualAd).all()
    
# PUT: Update active status of a visual ad by ID
class VisualAdActiveUpdate(BaseModel):
	active: bool

@router.put("/{ad_id}/active", response_model=VisualAdResponse)
def update_visual_ad_active(ad_id: int, data: VisualAdActiveUpdate, db: Session = Depends(get_db)):
	ad = db.query(VisualAd).filter(VisualAd.id == ad_id).first()
	if not ad:
		raise HTTPException(status_code=404, detail="Visual Ad not found")
	ad.active = data.active
	db.commit()
	db.refresh(ad)
	return ad
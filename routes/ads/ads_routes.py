from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

from db import get_db
from models.ads.ads_models import Ad

router = APIRouter(prefix="/api/ads", tags=["Ads"])


# Pydantic Schemas
class AdCreate(BaseModel):
    image: str  # Base64 encoded
    heading: str
    tagline: Optional[str] = None
    website_link: Optional[str] = None


class AdUpdate(BaseModel):
    image: Optional[str] = None
    heading: Optional[str] = None
    tagline: Optional[str] = None
    website_link: Optional[str] = None


class AdResponse(BaseModel):
    id: int
    image: str
    heading: str
    tagline: Optional[str] = None
    website_link: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# POST: Create a new ad
@router.post("/", response_model=AdResponse, status_code=status.HTTP_201_CREATED)
def create_ad(data: AdCreate, db: Session = Depends(get_db)):
    ad = Ad(
        image=data.image,
        heading=data.heading,
        tagline=data.tagline,
        website_link=data.website_link,
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


# GET: Get all ads
@router.get("/", response_model=List[AdResponse])
def get_all_ads(db: Session = Depends(get_db)):
    ads = db.query(Ad).all()
    return ads


# GET: Get ad by id
@router.get("/{ad_id}", response_model=AdResponse)
def get_ad_by_id(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")
    return ad


# PUT: Update ad by id
@router.put("/{ad_id}", response_model=AdResponse)
def update_ad(ad_id: int, data: AdUpdate, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ad, key, value)
    db.commit()
    db.refresh(ad)
    return ad


# DELETE: Delete ad by id
@router.delete("/{ad_id}", status_code=status.HTTP_200_OK)
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")
    db.delete(ad)
    db.commit()
    return {"detail": "Ad deleted"}


# DELETE: Delete all ads
@router.delete("/", status_code=status.HTTP_200_OK)
def delete_all_ads(db: Session = Depends(get_db)):
    deleted = db.query(Ad).delete()
    db.commit()
    return {"detail": f"Deleted {deleted} ads"}

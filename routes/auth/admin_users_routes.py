from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from db import get_db
from models.auth.admin_users_models import AdminUser

router = APIRouter(prefix="/api/auth/admin-users", tags=["Admin Users"])


class AdminUserResponse(BaseModel):
    id: str

    class Config:
        from_attributes = True


class AdminLoginRequest(BaseModel):
    id: str
    password: str


class AdminLoginResponse(BaseModel):
    message: str
    admin: AdminUserResponse

    class Config:
        from_attributes = True


@router.post("/login", response_model=AdminLoginResponse)
def login_admin(data: AdminLoginRequest, db: Session = Depends(get_db)):
    """Login admin using id and password"""
    admin = db.query(AdminUser).filter(AdminUser.id == data.id).first()
    if not admin or admin.password != data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid id or password")

    return {"message": "Login successful", "admin": admin}


@router.get("/", response_model=List[AdminUserResponse])
def get_all_admins(db: Session = Depends(get_db)):
    """Return all admin users (IDs only)"""
    admins = db.query(AdminUser).all()
    return admins

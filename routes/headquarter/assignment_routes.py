from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from db import get_db
from models.headquarter.assignment_models import Assignment
from models.headquarter.headquarter_models import Headquarter
from models.auth.mr_users_models import MRUser

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])

class AssignmentCreate(BaseModel):
	mr_user_id: int
	headquarter_id: int
	date: datetime

class AssignmentUpdate(BaseModel):
	headquarter_id: Optional[int] = None
	date: Optional[datetime] = None

class AssignmentResponse(BaseModel):
	assignment_id: int
	mr_user_id: int
	headquarter_id: int
	date: datetime
	visit_status: str
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None
# GET headquarters details for MR user assignments
class HeadquarterInfo(BaseModel):
	headquarter_id: int
	name: str
	address: Optional[str] = None
	area_sales_manager_name: str
	contact_no: Optional[str] = None

	class Config:
		from_attributes = True

class AssignmentWithHQResponse(AssignmentResponse):
	headquarter: HeadquarterInfo

"""
GET: Fetch all headquarters (with full details) assigned to a given MR user.
Returns a list of assignments, each including headquarter details.
"""
@router.get("/mr-user/{mr_user_id}/headquarters", response_model=List[AssignmentWithHQResponse])
def get_headquarters_for_mr_user(mr_user_id: int, db: Session = Depends(get_db)):
	assignments = db.query(Assignment).filter(Assignment.mr_user_id == mr_user_id).all()
	results = []
	for assign in assignments:
		hq = db.query(Headquarter).filter(Headquarter.headquarter_id == assign.headquarter_id).first()
		hq_info = HeadquarterInfo(**hq.__dict__) if hq else None
		results.append(AssignmentWithHQResponse(
			**assign.__dict__,
			headquarter=hq_info
		))
	return results

# PUT visit status by MR user ID and assignment ID
from pydantic import constr

class VisitStatusUpdate(BaseModel):
	visit_status: constr(max_length=50)

"""
PUT: Update the visit status for a specific assignment by MR user ID and assignment ID.
Allows MR users to mark their visit status (e.g., pending, completed).
"""
@router.put("/mr-user/{mr_user_id}/assignment/{assignment_id}/visit-status", response_model=AssignmentResponse)
def update_visit_status(mr_user_id: int, assignment_id: int, data: VisitStatusUpdate, db: Session = Depends(get_db)):
	assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id, Assignment.mr_user_id == mr_user_id).first()
	if not assignment:
		raise HTTPException(status_code=404, detail="Assignment not found for this MR user")
	assignment.visit_status = data.visit_status
	db.commit()
	db.refresh(assignment)
	return assignment

	class Config:
		from_attributes = True

# POST
"""
POST: Create a new assignment for an MR user to visit a headquarter on a specific date.
Validates that both MR user and headquarter exist before creating the assignment.
"""
@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(data: AssignmentCreate, db: Session = Depends(get_db)):
	# Verify MR user and headquarter exist
	user = db.query(MRUser).filter(MRUser.id == data.mr_user_id).first()
	hq = db.query(Headquarter).filter(Headquarter.headquarter_id == data.headquarter_id).first()
	if not user:
		raise HTTPException(status_code=404, detail="MR User not found")
	if not hq:
		raise HTTPException(status_code=404, detail="Headquarter not found")
	assignment = Assignment(**data.model_dump())
	db.add(assignment)
	db.commit()
	db.refresh(assignment)
	return assignment

# GET all assignments for MR user
"""
GET: Fetch all assignments for a given MR user.
Returns a list of assignments (without headquarter details).
"""
@router.get("/mr-user/{mr_user_id}", response_model=List[AssignmentResponse])
def get_assignments_by_mr_user(mr_user_id: int, db: Session = Depends(get_db)):
	return db.query(Assignment).filter(Assignment.mr_user_id == mr_user_id).all()

# GET all assignments for headquarter
"""
GET: Fetch all assignments for a given headquarter.
Returns a list of assignments for the specified headquarter.
"""
@router.get("/headquarter/{headquarter_id}", response_model=List[AssignmentResponse])
def get_assignments_by_headquarter(headquarter_id: int, db: Session = Depends(get_db)):
	return db.query(Assignment).filter(Assignment.headquarter_id == headquarter_id).all()

# PUT
"""
PUT: Update assignment details (headquarter or date) by assignment ID.
Allows updating the headquarter or date for an existing assignment.
"""
@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(assignment_id: int, data: AssignmentUpdate, db: Session = Depends(get_db)):
	assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
	if not assignment:
		raise HTTPException(status_code=404, detail="Assignment not found")
	update_data = data.model_dump(exclude_unset=True)
	for key, value in update_data.items():
		setattr(assignment, key, value)
	db.commit()
	db.refresh(assignment)
	return assignment

# DELETE
"""
DELETE: Remove an assignment by assignment ID.
Deletes the assignment from the database if it exists.
"""
@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
	assignment = db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()
	if not assignment:
		raise HTTPException(status_code=404, detail="Assignment not found")
	db.delete(assignment)
	db.commit()

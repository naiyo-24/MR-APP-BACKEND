from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    from models.auth.mr_users_models import MRUser
    from models.auth.admin_users_models import AdminUser
    from models.attendance.attendance_models import Attendance
    from models.doctor.doctor_models import Doctor, Chamber
    from models.appointment.appointment_models import Appointment
    from models.headquarter.headquarter_models import Headquarter
    from models.headquarter.assignment_models import Assignment
    from models.visual_ads.visual_ads_models import VisualAd
    from models.salary_slip.slip_models import SalarySlip
    Base.metadata.create_all(bind=engine)

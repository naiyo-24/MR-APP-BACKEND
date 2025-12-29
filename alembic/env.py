# Alembic environment file
# This file will be configured to work with db.py, main.py, and .env

import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Ensure project root is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Import Base and all models for full metadata
from db import Base
from models.auth.mr_users_models import MRUser
from models.auth.admin_users_models import AdminUser
from models.attendance.attendance_models import Attendance
from models.doctor.doctor_models import Doctor
from models.doctor.chamber_models import Chamber
from models.appointment.appointment_models import Appointment
from models.headquarter.headquarter_models import Headquarter
from models.headquarter.assignment_models import Assignment
from models.visual_ads.visual_ads_models import VisualAd
from models.ads.ads_models import Ad
from models.salary_slip.slip_models import SalarySlip

target_metadata = Base.metadata

def get_url():
    # Try to get DATABASE_URL from .env, else build from components
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    # Fallback: build from individual .env variables (as in db.py)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    if all([db_user, db_password, db_host, db_port, db_name]):
        return f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    raise RuntimeError("DATABASE_URL or all DB_* variables must be set in .env")

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url()
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

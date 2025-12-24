# Medorica Pharma — MR App (Backend)

Brief backend for Medical Representative management built with FastAPI and SQLAlchemy.

**Features**
- Authentication: MR users and admin login/signup endpoints
- Attendance tracking with selfie proof and monthly summaries
- Doctor & Chamber management (doctors added by MR users)
- Appointment scheduling (MR user → doctor → chamber)
- Headquarters and assignment management
- Salary slip uploads (PDF base64) per MR user
- Visual ads and general advertisements management
- PostgreSQL database via SQLAlchemy

**Repository Structure (key files)**
- [main.py](main.py) — FastAPI app, router registration, CORS and lifespan hooks
- [db.py](db.py) — SQLAlchemy engine, Base, and `create_tables()`
- [requirements.txt](requirements.txt)
- models/ — SQLAlchemy models
  - [models/auth/mr_users_models.py](models/auth/mr_users_models.py)
  - [models/auth/admin_users_models.py](models/auth/admin_users_models.py)
  - [models/attendance/attendance_models.py](models/attendance/attendance_models.py)
  - [models/doctor/doctor_models.py](models/doctor/doctor_models.py)
  - [models/appointment/appointment_models.py](models/appointment/appointment_models.py)
  - [models/headquarter/headquarter_models.py](models/headquarter/headquarter_models.py)
  - [models/headquarter/assignment_models.py](models/headquarter/assignment_models.py)
  - [models/visual_ads/visual_ads_models.py](models/visual_ads/visual_ads_models.py)
  - [models/ads/ads_models.py](models/ads/ads_models.py)
  - [models/salary_slip/slip_models.py](models/salary_slip/slip_models.py)
- routes/ — API routers grouped by feature
  - [routes/auth/mr_users_routes.py](routes/auth/mr_users_routes.py)
  - [routes/auth/admin_users_routes.py](routes/auth/admin_users_routes.py)
  - [routes/attendance/attendance_routes.py](routes/attendance/attendance_routes.py)
  - [routes/doctor/doctor_routes.py](routes/doctor/doctor_routes.py)
  - [routes/doctor/chamber_routes.py](routes/doctor/chamber_routes.py)
  - [routes/appointment/appointment_routes.py](routes/appointment/appointment_routes.py)
  - [routes/headquarter/headquarter_routes.py](routes/headquarter/headquarter_routes.py)
  - [routes/headquarter/assignment_routes.py](routes/headquarter/assignment_routes.py)
  - [routes/visual_ads/visual_ads_routes.py](routes/visual_ads/visual_ads_routes.py)
  - [routes/salary_slip/slip_routes.py](routes/salary_slip/slip_routes.py)
  - [routes/ads/ads_routes.py](routes/ads/ads_routes.py)

**API Endpoints (summary)**
Note: all routes are prefixed as shown in each router. Use `/docs` for interactive docs.

- Auth — MR Users (`/api/auth/mr-users`)
  - POST `/signup` — create MR user
  - POST `/login` — login MR user
  - GET `/` — list MR users
  - GET `/{user_id}` — get MR user by id
  - PUT `/{user_id}/...` — update fields (full-name, phone-no, email, address, headquarters, password, bank-ac-no, bank-ifsc-code, bank-name, branch-name, upi-id, date-of-birth, gender, profile-photo, alternative-phone-no, designation, is-verified)
  - PUT `/{user_id}` — bulk update

- Auth — Admin (`/api/auth/admin-users`)
  - POST `/login` — admin login (id + password)
  - GET `/` — list admin IDs

- Attendance (`/api/attendance`)
  - POST `/` — create attendance record
  - GET `/` — list all attendance
  - GET `/{attendance_id}` — get attendance by id
  - GET `/user/{user_id}` — attendance for MR user
  - GET `/user/{user_id}/date/{date}` — attendance for user on date
  - PUT `/{attendance_id}/check-in-time` — update check-in
  - PUT `/{attendance_id}/check-out-time` — update check-out
  - PUT `/{attendance_id}/selfie-proof` — update selfie (base64)
  - PUT `/{attendance_id}/present` — update present flag
  - PUT `/admin/user/{user_id}/date/{date}/present` — admin set/create present
  - PUT `/{attendance_id}` — bulk update attendance
  - GET `/summary/user/{user_id}/month/{year}/{month}` — monthly summary

- Doctor (`/api/doctor`) and Chamber (`/api/chamber`)
  - POST `/api/doctor/mr-user/{mr_user_id}` — add doctor for MR
  - GET `/api/doctor/mr-user/{mr_user_id}` — doctors by MR user
  - GET `/api/doctor/` — all doctors
  - PUT `/api/doctor/{doctor_id}` — update doctor (and chambers)
  - POST `/api/chamber/` — add chamber
  - GET `/api/chamber/` — all chambers
  - GET `/api/chamber/doctor/{doctor_id}` — chambers by doctor
  - PUT `/api/chamber/{chamber_id}` — update chamber

- Appointment (`/api/appointment`)
  - POST `/mr-user/{mr_user_id}` — create appointment
  - GET `/mr-user/{mr_user_id}` — appointments for MR (with doctor & chamber)
  - PUT `/mr-user/{mr_user_id}/appointment/{appointment_id}` — update appointment

- Headquarters (`/api/headquarters`) and Assignments (`/api/assignments`)
  - POST `/api/headquarters/` — create headquarter
  - GET `/api/headquarters/` — list HQs
  - GET `/api/headquarters/{headquarter_id}` — get HQ
  - PUT `/api/headquarters/{headquarter_id}` — update HQ
  - DELETE `/api/headquarters/{headquarter_id}` — delete HQ
  - POST `/api/assignments/` — create assignment (MR ↔ HQ)
  - GET `/api/assignments/mr-user/{mr_user_id}/headquarters` — HQ details for MR
  - GET `/api/assignments/mr-user/{mr_user_id}` — assignments for MR
  - GET `/api/assignments/headquarter/{headquarter_id}` — assignments for HQ
  - PUT `/api/assignments/mr-user/{mr_user_id}/assignment/{assignment_id}/visit-status` — update visit status
  - PUT `/api/assignments/{assignment_id}` — update assignment
  - DELETE `/api/assignments/{assignment_id}` — delete assignment

- Visual Ads (`/api/visual-ads`)
  - POST `/` — create visual ad
  - GET `/{ad_id}` — get visual ad
  - GET `/` — list visual ads
  - PUT `/{ad_id}/active` — toggle active

- Salary Slip (`/api/salary-slip`)
  - POST `/` — create salary slip (pdf base64)
  - GET `/` — list all slips
  - GET `/mr-user/{mr_user_id}` — slips by MR user
  - PUT `/{slip_id}` — update slip
  - DELETE `/{slip_id}` — delete slip

- Ads (`/api/ads`)
  - POST `/` — create ad
  - GET `/` — list ads
  - GET `/{ad_id}` — get ad
  - PUT `/{ad_id}` — update ad
  - DELETE `/{ad_id}` — delete ad
  - DELETE `/` — delete all ads

**Database model overview**
Tables and main fields (SQLAlchemy models)
- `mr_users` (`MRUser`): id, full_name, phone_no (unique), email (unique), password, address, headquarters, bank fields, upi_id, date_of_birth, gender, profile_photo (base64), designation, is_verified, created_at, updated_at, last_login
- `admin_users` (`AdminUser`): id (string, primary key), password
- `attendance` (`Attendance`): attendance_id, id (FK→mr_users.id), name, check_in_time, check_out_time, date, selfie_proof, present
- `doctors` (`Doctor`): doctor_id, mr_user_id (FK→mr_users.id), doctor_name, phone_no, email, address, qualification, specialization, experience
- `chambers` (`Chamber`): chamber_id, doctor_id (FK→doctors.doctor_id), chamber_name, chamber_address, chamber_phone_no
- `appointments` (`Appointment`): appointment_id, mr_user_id, doctor_id, chamber_id, date, time, status, notes
- `headquarters` (`Headquarter`): headquarter_id, name, address, area_sales_manager_name, contact_no
- `assignments` (`Assignment`): assignment_id, mr_user_id, headquarter_id, date, visit_status
- `visual_ads` (`VisualAd`): id, med_name, photo_url (base64), active
- `advertisements` (`Ad`): id, image (base64), heading, tagline, website_link
- `salary_slips` (`SalarySlip`): id, mr_user_id, month, year, pdf_base64

Relationships: foreign keys link MR users → attendance/appointments/assignments/salary_slips; doctors → chambers → appointments.

**Environment variables (.env)**
Minimum required for DB connection (place in `.env` in project root):

- `DB_HOST` — PostgreSQL host (e.g., localhost)
- `DB_PORT` — PostgreSQL port (e.g., 5432)
- `DB_NAME` — database name
- `DB_USER` — DB username
- `DB_PASSWORD` — DB password

Optional / recommended:
- `APP_ENV` — development/production
- `UVICORN_PORT` — port to run uvicorn
- `SECRET_KEY` — app secret if you add JWTs later

Example `.env`:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=mr_app_db
DB_USER=postgres
DB_PASSWORD=changeme

**Run locally (venv) — macOS / Linux**

1. Create and activate venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create `.env` (see above) and ensure PostgreSQL is reachable

4. Create DB tables and run server

```bash
# option A: run using main entry (uses uvicorn settings within main.py)
python main.py

# option B: explicit uvicorn (port 8000)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Run locally — Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
# then same run commands as above
python main.py
```

**Notes & Tips**
- The project expects a PostgreSQL server; adjust `DB_*` in `.env` accordingly.
- Interactive API docs available at [http://localhost:8000/docs](http://localhost:8000/docs) (or port set in `main.py`).
- Passwords are currently stored and validated in plain text (see `routes/auth/*`). For production, implement hashing and secure auth (bcrypt / JWT).
- Large binary fields are stored as base64 in text columns (images, pdfs). Consider storing files in object storage for production.

If you want, I can:
- Add a `Makefile` or `scripts/` for common commands
- Add a `docker-compose.yml` with a Postgres service for local dev
- Harden authentication (password hashing + JWT)

---
Generated by repository analysis. Ask me to tweak sections or add examples. 

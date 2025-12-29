# Medorica Pharma Pvt Ltd - MR App Backend

## Features
- User authentication for Medical Representatives (MR) and Admins
- Attendance management with check-in/check-out and selfie proof
- Doctor and chamber management
- Appointment scheduling and management
- Headquarter and assignment management
- Visual ads and advertisements management
- Salary slip upload and retrieval
- Force update APK delivery for mobile app
- Admin and MR user profile management
- Monthly attendance summary and reporting
- RESTful API with FastAPI and SQLAlchemy ORM
- Alembic migrations for database schema
- Docker and docker-compose support

## Setup & Running the Project

### 1. Clone the repository
```bash
git clone <repo-url>
cd MR-APP-BACKEND
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medorica_mr_db
DB_USER=postgres
DB_PASSWORD=2004
```

### 5. Run database migrations (optional, if using Alembic)
```bash
alembic upgrade head
```

### 6. Start the backend server
```bash
uvicorn main:app --host 0.0.0.0 --port 2000 --reload
```

Or use Docker Compose:
```bash
docker-compose up --build
```

## Project File Structure
```
MR-APP-BACKEND/
├── alembic/                # Alembic migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── models/                 # SQLAlchemy models
│   ├── ads/
│   ├── appointment/
│   ├── attendance/
│   ├── auth/
│   ├── doctor/
│   ├── headquarter/
│   ├── salary_slip/
│   └── visual_ads/
├── routes/                 # FastAPI routers
│   ├── ads/
│   ├── appointment/
│   ├── attendance/
│   ├── auth/
│   ├── doctor/
│   ├── headquarter/
│   ├── salary_slip/
│   ├── updates/
│   └── visual_ads/
├── db.py                   # Database connection and helpers
├── main.py                 # FastAPI app entrypoint
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker Compose config
├── Dockerfile              # Docker build file
├── alembic.ini             # Alembic config
├── .env                    # Environment variables
└── README.md               # Project documentation
```

## API Endpoints (Summary)

### Auth (MR & Admin)
- `POST /api/auth/mr-users/signup` - MR user registration
- `POST /api/auth/mr-users/login` - MR user login
- `GET /api/auth/mr-users/` - List all MR users
- `GET /api/auth/mr-users/{user_id}` - Get MR user by ID
- `PUT /api/auth/mr-users/{user_id}` - Update MR user fields
- `POST /api/auth/admin-users/login` - Admin login
- `GET /api/auth/admin-users/` - List all admin users

### Attendance
- `POST /api/attendance/` - Create attendance record
- `GET /api/attendance/` - List all attendance records
- `GET /api/attendance/{attendance_id}` - Get attendance by ID
- `GET /api/attendance/user/{user_id}` - Get attendance for MR user
- `PUT /api/attendance/{attendance_id}` - Update attendance fields
- `PUT /api/attendance/{attendance_id}/check-in-time` - Update check-in time
- `PUT /api/attendance/{attendance_id}/check-out-time` - Update check-out time
- `PUT /api/attendance/{attendance_id}/selfie-proof` - Update selfie proof
- `PUT /api/attendance/{attendance_id}/present` - Update present status
- `GET /api/attendance/summary/user/{user_id}/month/{year}/{month}` - Monthly summary

### Doctor & Chamber
- `POST /api/doctor/mr-user/{mr_user_id}` - Add doctor for MR
- `GET /api/doctor/mr-user/{mr_user_id}` - List doctors for MR
- `GET /api/doctor/` - List all doctors
- `PUT /api/doctor/{doctor_id}` - Update doctor
- `POST /api/chamber/` - Add chamber
- `GET /api/chamber/` - List all chambers
- `GET /api/chamber/doctor/{doctor_id}` - List chambers for doctor
- `PUT /api/chamber/{chamber_id}` - Update chamber

### Appointment
- `POST /api/appointment/mr-user/{mr_user_id}` - Create appointment
- `GET /api/appointment/mr-user/{mr_user_id}` - List appointments for MR
- `PUT /api/appointment/mr-user/{mr_user_id}/appointment/{appointment_id}` - Update appointment

### Headquarter & Assignment
- `POST /api/headquarters/` - Create headquarter
- `GET /api/headquarters/` - List all headquarters
- `PUT /api/headquarters/{headquarter_id}` - Update headquarter
- `DELETE /api/headquarters/{headquarter_id}` - Delete headquarter
- `POST /api/assignments/` - Create assignment
- `GET /api/assignments/mr-user/{mr_user_id}` - List assignments for MR
- `GET /api/assignments/headquarter/{headquarter_id}` - List assignments for headquarter
- `PUT /api/assignments/{assignment_id}` - Update assignment
- `DELETE /api/assignments/{assignment_id}` - Delete assignment
- `PUT /api/assignments/mr-user/{mr_user_id}/assignment/{assignment_id}/visit-status` - Update visit status

### Visual Ads & Ads
- `POST /api/visual-ads/` - Create visual ad
- `GET /api/visual-ads/` - List all visual ads
- `PUT /api/visual-ads/{ad_id}/active` - Update visual ad active status
- `POST /api/ads/` - Create ad
- `GET /api/ads/` - List all ads
- `PUT /api/ads/{ad_id}` - Update ad
- `DELETE /api/ads/{ad_id}` - Delete ad

### Salary Slip
- `POST /api/salary-slip/` - Upload salary slip
- `GET /api/salary-slip/` - List all salary slips
- `GET /api/salary-slip/mr-user/{mr_user_id}` - List salary slips for MR
- `PUT /api/salary-slip/{slip_id}` - Update salary slip
- `DELETE /api/salary-slip/{slip_id}` - Delete salary slip

### Force Update
- `GET /api/force-update/` - Get latest APK info
- `GET /api/force-update/download-apk/{filename}` - Download APK by filename
- `GET /api/force-update/download-apk` - Download latest APK

### Health & Root
- `GET /` - API root (welcome)
- `GET /health` - Health check

## FastAPI Documentation
- Interactive API docs: [http://localhost:2000/docs](http://localhost:2000/docs)
- ReDoc docs: [http://localhost:2000/redoc](http://localhost:2000/redoc)
- OpenAPI schema: [http://localhost:2000/openapi.json](http://localhost:2000/openapi.json)

## Future Scope
- Role-based access control (RBAC) for more granular permissions
- Notification and messaging system
- Integration with external APIs (e.g., SMS, email)
- Advanced analytics and reporting
- Mobile push notification support
- Automated testing and CI/CD pipeline
- Multi-language support
- Enhanced security and audit logging

## Contact Us
For queries or support, contact:
- Naiyo24 Pvt. Ltd. Developer Team
- Email: naiyooffice@gmail.com

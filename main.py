from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import time

from db import create_tables
from routes.auth.mr_users_routes import router as mr_users_router
from routes.auth.admin_users_routes import router as admin_users_router
from routes.attendance.attendance_routes import router as attendance_router
from routes.doctor.doctor_routes import router as doctor_router
from routes.doctor.chamber_routes import router as chamber_router
from routes.appointment.appointment_routes import router as appointment_router
from routes.headquarter.headquarter_routes import router as headquarter_router
from routes.headquarter.assignment_routes import router as assignment_router
from routes.visual_ads.visual_ads_routes import router as visual_ads_router
from routes.salary_slip.slip_routes import router as salary_slip_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    create_tables()
    logger.info("Database tables created successfully!")
    logger.info("Server is running and accepting requests from all networks (0.0.0.0)")
    yield
    # Shutdown: cleanup if needed
    logger.info("Application shutting down...")


app = FastAPI(
    title="Medorica Pharma Pvt Ltd - MR App",
    description="Backend for Medical Representative Management Application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration - Accept requests from any origin/port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accept from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)


# Middleware to log all API requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"📥 {request.method} {request.url.path} - Client: {request.client.host}:{request.client.port}")
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response


 # Include routers




app.include_router(mr_users_router)
app.include_router(admin_users_router)
app.include_router(attendance_router)
app.include_router(doctor_router)
app.include_router(chamber_router)
app.include_router(appointment_router)
app.include_router(headquarter_router)
app.include_router(assignment_router)
app.include_router(visual_ads_router)
app.include_router(salary_slip_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Medorica Pharma Pvt Ltd - MR App API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=2000, reload=True)

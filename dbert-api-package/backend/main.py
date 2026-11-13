from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from backend.api.docs_landing import get_developer_hub_html, get_api_manifest_json
from backend.core.config import settings
from backend.core.middleware import RequestContextMiddleware, logger
from backend.core.database import engine
from backend.api.v1.auth.router import router as auth_router
from backend.api.v1.intern.router import router as intern_router
from backend.api.v1.applications.router import router as applications_router
from backend.api.v1.enrollments.router import router as enrollments_router
from backend.api.v1.payments.router import router as payments_router
from backend.api.v1.uploads.router import router as uploads_router, get_uploaded_file
from backend.api.v1.intern.interview_router import router as interview_router
from backend.api.v1.courses.router import router as courses_router
from backend.api.v1.learning.router import router as learning_router
from backend.api.v1.admin.router import router as admin_router
from backend.api.v1.cron.router import router as cron_router
from backend.api.v1.messaging.router import router as messaging_router
from backend.api.v1.notifications.router import router as notifications_router
from backend.api.v1.credentials.router import router as credentials_router
from backend.api.v1.ambassador.router import router as ambassador_router
from backend.api.v1.tasks.router import router as tasks_router
from backend.api.v1.company.router import router as company_router
from backend.api.v1.marketplace.router import router as marketplace_router
from backend.api.v1.public.router import router as public_router

openapi_tags = [
    {"name": "Health & Probes", "description": "Liveness and readiness health checks"},
    {"name": "Auth & Security", "description": "Authentication for Intern, Company, Mentor, Staff, Admin"},
    {"name": "Intern Workspace", "description": "Intern profile, applications, interview, and progress"},
    {"name": "Applications", "description": "Application submission and lifecycle state transitions"},
    {"name": "Enrollments", "description": "Enrollment deposits and verification workflows"},
    {"name": "Payments", "description": "Razorpay order generation, webhooks, and verification"},
    {"name": "Courses & Guided Learning", "description": "Course catalog, chapters, quizzes, and AI tutor dialogs"},
    {"name": "Company & Employer", "description": "Company registration, post authoring, candidate screening"},
    {"name": "Mentor Network", "description": "Mentor review queues and session booking"},
    {"name": "Staff Operations", "description": "Staff queues for project submissions and mentor slots"},
    {"name": "Admin Control Plane", "description": "Platform management, CSV exports, user administration"},
    {"name": "Job Marketplace", "description": "Public internship and job listings"},
    {"name": "Messaging & Alerts", "description": "Real-time inboxes and notification center"},
    {"name": "CV & Credentials", "description": "Dynamic CV generation and public certificate validation"},
    {"name": "Scheduled Cron", "description": "Automated background cleanup and reminder dispatch"}
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")
    await engine.dispose()

API_DESCRIPTION = """
## Welcome to DBERT Sovereign REST API (`api.dbert.in`)

Official high-performance REST API powering DBERT's sovereign digital credentials, internship tracking, course learning management, pedagogical AI tutor dialogs, and 6,600+ curated tech marketplace opportunities.

### 🚀 Developer Quickstart
- **Base URL**: `https://api.dbert.in/api/v1`
- **Interactive Documentation**: [`https://api.dbert.in/docs`](https://api.dbert.in/docs) (Swagger UI)
- **Technical Specification**: [`https://api.dbert.in/redoc`](https://api.dbert.in/redoc) (ReDoc)
- **OpenAPI Schema**: [`https://api.dbert.in/openapi.json`](https://api.dbert.in/openapi.json)
- **Service Probes**: [`/health`](https://api.dbert.in/health), [`/ready`](https://api.dbert.in/ready), [`/status`](https://api.dbert.in/status)

### 🔑 Authentication Guide
Include your signed JWT bearer token in the `Authorization` header for all protected endpoints:
```http
Authorization: Bearer <your_jwt_access_token>
Content-Type: application/json
```
To obtain tokens:
- **Interns / Candidates**: `POST /api/v1/auth/intern/login`
- **Hiring Companies**: `POST /api/v1/auth/company/login`
- **Mentors & Faculty**: `POST /api/v1/auth/mentor/login`
- **Staff Operations**: `POST /api/v1/auth/staff/login`
"""

app = FastAPI(
    title="DBERT Ecosystem REST API",
    summary="Sovereign REST API for DBERT Credentials, LMS, Marketplace, and AI Learning",
    description=API_DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=openapi_tags,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "DBERT Engineering & Developer Platform",
        "url": "https://dbert.in",
        "email": "engineering@dbert.in"
    },
    license_info={
        "name": "Proprietary Developer Access",
        "url": "https://dbert.in/terms"
    },
    servers=[
        {"url": "https://api.dbert.in", "description": "Production Sovereign API Server"},
        {"url": "http://127.0.0.1:8000", "description": "Local Development Server"}
    ]
)

# Middleware: Request Context & Tracing
app.add_middleware(RequestContextMiddleware)

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(intern_router, prefix=settings.API_V1_STR)
app.include_router(applications_router, prefix=settings.API_V1_STR)
app.include_router(enrollments_router, prefix=settings.API_V1_STR)
app.include_router(payments_router, prefix=settings.API_V1_STR)
app.include_router(uploads_router, prefix=settings.API_V1_STR)
app.include_router(interview_router, prefix=settings.API_V1_STR)
app.include_router(courses_router, prefix=settings.API_V1_STR)
app.include_router(learning_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(cron_router, prefix=settings.API_V1_STR)
app.include_router(messaging_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(credentials_router, prefix=settings.API_V1_STR)
app.include_router(ambassador_router, prefix=settings.API_V1_STR)
app.include_router(tasks_router, prefix=settings.API_V1_STR)
app.include_router(company_router, prefix=settings.API_V1_STR)
app.include_router(marketplace_router, prefix=settings.API_V1_STR)
app.include_router(public_router, prefix=settings.API_V1_STR)

# Top-level /uploads route for direct image/PDF rendering
app.add_api_route("/uploads/{filename}", get_uploaded_file, methods=["GET"], tags=["File Storage"])


@app.get("/", tags=["Developer Platform"], summary="Developer Portal & API Instructions")
async def developer_landing(request: Request):
    """
    Developer Platform Hub & Instructions for api.dbert.in.
    Renders an interactive developer portal with complete API instructions,
    or returns structured JSON if Accept: application/json or ?format=json.
    """
    accept = request.headers.get("accept", "")
    format_arg = request.query_params.get("format", "").lower()
    if "application/json" in accept or format_arg == "json":
        return JSONResponse(content=get_api_manifest_json(settings.VERSION, settings.ENVIRONMENT))
    return HTMLResponse(content=get_developer_hub_html(settings.VERSION, settings.ENVIRONMENT))


@app.get("/instructions", tags=["Developer Platform"], summary="Full API Instructions")
async def developer_instructions():
    """Renders the comprehensive API Instructions guide for developers building on DBERT."""
    return HTMLResponse(content=get_developer_hub_html(settings.VERSION, settings.ENVIRONMENT))


@app.get("/api", tags=["Developer Platform"], summary="API Version Index")
@app.get("/api/v1", tags=["Developer Platform"], summary="API v1 Manifest")
async def api_manifest_index():
    """Returns the API discovery manifest and core modules directory."""
    return JSONResponse(content=get_api_manifest_json(settings.VERSION, settings.ENVIRONMENT))

@app.get("/health", tags=["Health & Probes"], summary="Liveness Health Check")
async def health_check():
    """Liveness probe to confirm HTTP service responsiveness."""
    return {"status": "ok", "service": "dbert-api", "version": settings.VERSION}

@app.get("/ready", tags=["Health & Probes"], summary="Readiness Probe")
async def readiness_check():
    """Readiness probe checking database connectivity."""
    try:
        # Ping the database engine connection
        async with engine.connect() as conn:
            return {"status": "ready", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": str(e)}
        )

@app.get("/status", tags=["Health & Probes"], summary="Full System Status")
async def system_status():
    """Returns general service health metadata."""
    return {
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
        "interviews_enabled": settings.INTERVIEW_ENABLED,
        "emails_enabled": settings.EMAILS_ENABLED
    }

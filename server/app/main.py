from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
import sys
import time

from app.config import settings
from app.database import init_db
from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router


logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG" if settings.ENVIRONMENT == "development" else "INFO",
    colorize=True,
)
logger.add("logs/app.log", rotation="10 MB", retention="30 days", compression="gz", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Task API server...")
    await init_db()
    logger.info("Database initialized")
    await seed_admin()
    yield
    logger.info("Shutting down Task API server...")


async def seed_admin():
    from app.database import AsyncSessionLocal
    from app.models.user import User, UserRole
    from app.middleware.security import hash_password
    from sqlalchemy import select

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        if not result.scalar_one_or_none():
            admin = User(
                email=settings.ADMIN_EMAIL, name=settings.ADMIN_NAME,
                password=hash_password(settings.ADMIN_PASSWORD), role=UserRole.ADMIN,
            )
            session.add(admin)
            await session.commit()
            logger.info(f"Admin user seeded: {settings.ADMIN_EMAIL}")
        else:
            logger.info(f"Admin user already exists: {settings.ADMIN_EMAIL}")


app = FastAPI(
    title="Task API",
    description=(
        "Scalable REST API with JWT Authentication & Role-Based Access Control.\n\n"
        "## Features\n"
        "- User Registration & Login with bcrypt password hashing\n"
        "- JWT Access Tokens (15min) + Refresh Tokens (7 days)\n"
        "- Role-Based Access Control (USER / ADMIN)\n"
        "- Task CRUD with ownership enforcement\n"
        "- Pagination, Search & Filtering\n"
        "- Input Validation via Pydantic\n\n"
        "## Getting Started\n"
        "1. Register via `POST /api/v1/auth/register`\n"
        "2. Login via `POST /api/v1/auth/login` to get your JWT\n"
        "3. Click **Authorize** above and enter your token\n"
        "4. All `/tasks` endpoints are now accessible"
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({"field": field, "message": error["msg"]})
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"success": False, "error": "Validation failed", "details": errors},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    detail = "Internal server error" if settings.ENVIRONMENT == "production" else str(exc)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"success": False, "error": detail})


app.include_router(auth_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")


@app.get("/health", tags=["Health"], summary="Health check")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "environment": settings.ENVIRONMENT}


@app.get("/", tags=["Root"], include_in_schema=False)
async def root():
    return {"message": "Task API v1.0.0", "docs": "/api/docs", "health": "/health"}

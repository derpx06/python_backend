from typing import Annotated
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.middleware.auth import CurrentUser

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201, summary="Register a new user")
async def register(data: UserRegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await AuthService.register(db, data)
    return {"success": True, "message": "User registered successfully.", "data": {"user": user}}


@router.post("/login", summary="Login and get JWT tokens")
async def login(data: UserLoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await AuthService.login(db, data)
    return {"success": True, "message": "Login successful.", "data": result}


@router.get("/me", summary="Get current user profile")
async def get_profile(current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    profile = await AuthService.get_profile(db, current_user.id)
    return {"success": True, "data": {"user": profile}}


@router.post("/refresh", summary="Refresh access token")
async def refresh_token(
    refresh_token: Annotated[str, Body(..., embed=True)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await AuthService.refresh_token(db, refresh_token)
    return {"success": True, "data": result}

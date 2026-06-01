from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from app.models.user import User
from app.models.task import Task
from app.middleware.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from loguru import logger


class AuthService:

    @staticmethod
    async def register(db: AsyncSession, data: UserRegisterRequest) -> dict:
        result = await db.execute(select(User).where(User.email == data.email.lower()))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists.")

        hashed = hash_password(data.password)
        user = User(email=data.email.lower().strip(), name=data.name.strip(), password=hashed)
        db.add(user)
        await db.flush()
        await db.refresh(user)

        logger.info(f"New user registered: {user.email} (ID: {user.id})")
        return {"id": user.id, "email": user.email, "name": user.name, "role": user.role.value, "created_at": user.created_at.isoformat()}

    @staticmethod
    async def login(db: AsyncSession, data: UserLoginRequest) -> dict:
        result = await db.execute(select(User).where(User.email == data.email.lower()))
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

        token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        logger.info(f"User logged in: {user.email} (ID: {user.id})")
        return {
            "user": {"id": user.id, "email": user.email, "name": user.name, "role": user.role.value},
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    async def get_profile(db: AsyncSession, user_id: int) -> dict:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        task_count_result = await db.execute(select(func.count(Task.id)).where(Task.owner_id == user_id))
        task_count = task_count_result.scalar() or 0

        return {
            "id": user.id, "email": user.email, "name": user.name, "role": user.role.value,
            "created_at": user.created_at.isoformat(), "updated_at": user.updated_at.isoformat(),
            "task_count": task_count,
        }

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token_str: str) -> dict:
        payload = decode_refresh_token(refresh_token_str)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token.")

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload.")

        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists.")

        token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
        return {"access_token": create_access_token(token_data), "token_type": "bearer"}

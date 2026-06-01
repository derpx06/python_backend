from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from app.models.task import Task, TaskStatus
from app.models.user import User, UserRole
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest
from loguru import logger


class TaskService:

    @staticmethod
    async def create_task(db: AsyncSession, data: TaskCreateRequest, owner_id: int) -> dict:
        task = Task(
            title=data.title.strip(),
            description=data.description.strip() if data.description else None,
            status=data.status,
            owner_id=owner_id,
        )
        db.add(task)
        await db.flush()
        await db.refresh(task)
        logger.info(f"Task created: '{task.title}' (ID: {task.id}) by user {owner_id}")
        return _serialize_task(task)

    @staticmethod
    async def get_tasks(
        db: AsyncSession, user: User,
        page: int = 1, limit: int = 20,
        status_filter: Optional[TaskStatus] = None,
        search: Optional[str] = None,
    ) -> dict:
        query = select(Task)

        if user.role != UserRole.ADMIN:
            query = query.where(Task.owner_id == user.id)
        if status_filter:
            query = query.where(Task.status == status_filter)
        if search:
            query = query.where(Task.title.ilike(f"%{search}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0

        offset = (page - 1) * limit
        query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)
        tasks = (await db.execute(query)).scalars().all()

        return {
            "tasks": [_serialize_task(t) for t in tasks],
            "meta": {
                "total": total, "page": page, "limit": limit,
                "total_pages": (total + limit - 1) // limit if limit > 0 else 0,
            },
        }

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: int, user: User) -> dict:
        task = await _get_task_or_404(db, task_id)
        _check_ownership(task, user)
        return _serialize_task(task)

    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, data: TaskUpdateRequest, user: User) -> dict:
        task = await _get_task_or_404(db, task_id)
        _check_ownership(task, user)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(task, field, value.strip() if isinstance(value, str) else value)

        await db.flush()
        await db.refresh(task)
        logger.info(f"Task updated: ID {task.id} by user {user.id}")
        return _serialize_task(task)

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int, user: User) -> None:
        task = await _get_task_or_404(db, task_id)
        _check_ownership(task, user)
        await db.delete(task)
        await db.flush()
        logger.info(f"Task deleted: ID {task_id} by user {user.id}")


async def _get_task_or_404(db: AsyncSession, task_id: int) -> Task:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task


def _check_ownership(task: Task, user: User) -> None:
    if user.role != UserRole.ADMIN and task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this task.")


def _serialize_task(task: Task) -> dict:
    return {
        "id": task.id, "title": task.title, "description": task.description,
        "status": task.status.value, "owner_id": task.owner_id,
        "created_at": task.created_at.isoformat(), "updated_at": task.updated_at.isoformat(),
    }

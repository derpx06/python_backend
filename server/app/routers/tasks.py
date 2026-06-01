from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest
from app.models.task import TaskStatus
from app.middleware.auth import CurrentUser

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", status_code=201, summary="Create a new task")
async def create_task(
    data: TaskCreateRequest,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    task = await TaskService.create_task(db, data, current_user.id)
    return {"success": True, "message": "Task created successfully.", "data": {"task": task}}


@router.get("", summary="List tasks with pagination, filtering, and search")
async def list_tasks(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[Optional[TaskStatus], Query()] = None,
    search: Annotated[Optional[str], Query()] = None,
):
    result = await TaskService.get_tasks(db, current_user, page=page, limit=limit, status_filter=status, search=search)
    return {"success": True, "data": {"tasks": result["tasks"]}, "meta": result["meta"]}


@router.get("/{task_id}", summary="Get a task by ID")
async def get_task(
    task_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    task = await TaskService.get_task_by_id(db, task_id, current_user)
    return {"success": True, "data": {"task": task}}


@router.put("/{task_id}", summary="Update a task")
async def update_task(
    task_id: int,
    data: TaskUpdateRequest,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    task = await TaskService.update_task(db, task_id, data, current_user)
    return {"success": True, "message": "Task updated successfully.", "data": {"task": task}}


@router.delete("/{task_id}", status_code=204, summary="Delete a task")
async def delete_task(
    task_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await TaskService.delete_task(db, task_id, current_user)

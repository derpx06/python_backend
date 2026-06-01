from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.task import TaskStatus


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Complete the project"])
    description: Optional[str] = Field(None, max_length=5000, examples=["Finish all remaining features"])
    status: TaskStatus = Field(default=TaskStatus.TODO, examples=["TODO"])


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    success: bool = True
    data: list[TaskResponse]
    meta: dict = {}

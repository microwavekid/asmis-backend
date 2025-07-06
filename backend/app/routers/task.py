from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.connection import get_async_db_session
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_async_db_session)):
    """Stub: List all tasks (to be implemented)."""
    # TODO: Implement task listing logic
    return []

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: AsyncSession = Depends(get_async_db_session)):
    """Stub: Get a task by ID (to be implemented)."""
    # TODO: Implement get task logic
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_async_db_session)):
    """Stub: Create a new task (to be implemented)."""
    # TODO: Implement create task logic
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskUpdate, db: AsyncSession = Depends(get_async_db_session)):
    """Stub: Update a task (to be implemented)."""
    # TODO: Implement update task logic
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.delete("/{task_id}")
async def delete_task(task_id: str, db: AsyncSession = Depends(get_async_db_session)):
    """Stub: Delete a task (to be implemented)."""
    # TODO: Implement delete task logic
    raise HTTPException(status_code=501, detail="Not implemented yet") 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import sys
sys.path.append('src')
from src.database import get_db
from src.models import Task, User
from src.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from src.crud import create_task, get_task, get_user_tasks, update_task, delete_task
from src.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """List all tasks for current user."""
    tasks = await get_user_tasks(db, current_user_id)
    return {
        "tasks": tasks,
        "total": len(tasks)
    }


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Create new task."""
    task_data_dict = task_data.model_dump()
    task_data_dict["user_id"] = current_user_id
    
    task = await create_task(db, task_data_dict)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Get task by ID."""
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Update task."""
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = task_data.model_dump(exclude_unset=True)
    updated_task = await update_task(db, task_id, update_data)
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """Delete task."""
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    await delete_task(db, task_id)

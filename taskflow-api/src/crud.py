from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Task, User, TaskStatus


async def create_task(db: AsyncSession, task_data: dict) -> Task:
    """Create new task."""
    task = Task(**task_data)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(db: AsyncSession, task_id: int) -> Task:
    """Get task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def get_user_tasks(db: AsyncSession, user_id: int) -> list:
    """Get all tasks for a user."""
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return list(result.scalars().all())


async def update_task(db: AsyncSession, task_id: int, task_data: dict) -> Task:
    """Update task."""
    task = await get_task(db, task_id)
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """Delete task."""
    task = await get_task(db, task_id)
    if task:
        await db.delete(task)
        await db.commit()
        return True
    return False


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    """Get user by email."""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: dict) -> User:
    """Create new user."""
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

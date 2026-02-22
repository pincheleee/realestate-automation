from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_current_admin_user
from app.db.session import get_db
from app.db.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()
user_repo = UserRepository()


@router.get("/me", response_model=UserSchema)
async def read_current_user(
    current_user: User = Depends(get_current_active_user),
):
    """Get current authenticated user."""
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_current_user(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update current authenticated user."""
    user = await user_repo.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/", response_model=List[UserSchema])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    """List all users (admin only)."""
    return await user_repo.get_multi(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """Get a specific user by ID."""
    user = await user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.db.repositories.property import PropertyRepository
from app.models.user import User
from app.schemas.property import Property as PropertySchema, PropertyCreate, PropertyUpdate

router = APIRouter()
property_repo = PropertyRepository()


@router.get("/", response_model=List[PropertySchema])
async def list_properties(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all properties."""
    return await property_repo.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=PropertySchema, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_in: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new property listing."""
    return await property_repo.create(db, obj_in=property_in)


@router.get("/search", response_model=List[PropertySchema])
async def search_properties(
    q: str = "",
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    property_type: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search properties with filters."""
    return await property_repo.search(
        db,
        query=q,
        min_price=min_price,
        max_price=max_price,
        location=location,
        property_type=property_type,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        skip=skip,
        limit=limit,
    )


@router.get("/featured", response_model=List[PropertySchema])
async def featured_properties(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get featured (most recent available) properties."""
    return await property_repo.get_featured(db, limit=limit)


@router.get("/{property_id}", response_model=PropertySchema)
async def read_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific property by ID."""
    prop = await property_repo.get(db, id=property_id)
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    return prop


@router.put("/{property_id}", response_model=PropertySchema)
async def update_property(
    property_id: int,
    property_in: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an existing property."""
    prop = await property_repo.get(db, id=property_id)
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    return await property_repo.update(db, db_obj=prop, obj_in=property_in)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a property listing."""
    prop = await property_repo.get(db, id=property_id)
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    await property_repo.remove(db, id=property_id)

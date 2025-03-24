from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.base import BaseRepository
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate

class PropertyRepository(BaseRepository[Property, PropertyCreate, PropertyUpdate]):
    def __init__(self):
        super().__init__(Property)

    async def get_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Property]:
        query = (
            select(Property)
            .filter(Property.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def search(
        self,
        db: AsyncSession,
        *,
        query: str,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        location: Optional[str] = None,
        property_type: Optional[str] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Property]:
        conditions = []
        
        if query:
            conditions.append(
                or_(
                    Property.title.ilike(f"%{query}%"),
                    Property.description.ilike(f"%{query}%")
                )
            )
        
        if min_price is not None:
            conditions.append(Property.price >= min_price)
        
        if max_price is not None:
            conditions.append(Property.price <= max_price)
        
        if location:
            conditions.append(Property.location.ilike(f"%{location}%"))
        
        if property_type:
            conditions.append(Property.property_type == property_type)
        
        if bedrooms:
            conditions.append(Property.bedrooms >= bedrooms)
        
        if bathrooms:
            conditions.append(Property.bathrooms >= bathrooms)
        
        conditions.append(Property.available == True)
        
        query = (
            select(Property)
            .filter(and_(*conditions))
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_mls_id(self, db: AsyncSession, *, mls_id: str) -> Optional[Property]:
        query = select(Property).filter(Property.mls_id == mls_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_featured(
        self, db: AsyncSession, *, limit: int = 10
    ) -> List[Property]:
        query = (
            select(Property)
            .filter(Property.available == True)
            .order_by(Property.created_at.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all() 
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.base import BaseRepository
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate

class LeadRepository(BaseRepository[Lead, LeadCreate, LeadUpdate]):
    def __init__(self):
        super().__init__(Lead)

    async def get_by_agent(
        self, db: AsyncSession, *, agent_id: int, skip: int = 0, limit: int = 100
    ) -> List[Lead]:
        query = (
            select(Lead)
            .filter(Lead.assigned_agent_id == agent_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_status(
        self, db: AsyncSession, *, status: LeadStatus, skip: int = 0, limit: int = 100
    ) -> List[Lead]:
        query = (
            select(Lead)
            .filter(Lead.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Lead]:
        query = select(Lead).filter(Lead.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_active_leads(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Lead]:
        active_statuses = [
            LeadStatus.NEW,
            LeadStatus.CONTACTED,
            LeadStatus.QUALIFIED,
            LeadStatus.NEGOTIATING,
        ]
        query = (
            select(Lead)
            .filter(Lead.status.in_(active_statuses))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def update_status(
        self, db: AsyncSession, *, lead_id: int, status: LeadStatus
    ) -> Lead:
        lead = await self.get(db, id=lead_id)
        if lead:
            lead.status = status
            await db.commit()
            await db.refresh(lead)
        return lead

    async def assign_agent(
        self, db: AsyncSession, *, lead_id: int, agent_id: int
    ) -> Lead:
        lead = await self.get(db, id=lead_id)
        if lead:
            lead.assigned_agent_id = agent_id
            await db.commit()
            await db.refresh(lead)
        return lead 
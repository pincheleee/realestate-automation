from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.db.repositories.lead import LeadRepository
from app.models.lead import LeadStatus
from app.models.user import User
from app.schemas.lead import Lead as LeadSchema, LeadCreate, LeadUpdate

router = APIRouter()
lead_repo = LeadRepository()


@router.get("/", response_model=List[LeadSchema])
async def list_leads(
    skip: int = 0,
    limit: int = 100,
    status: Optional[LeadStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List leads, optionally filtered by status."""
    if status:
        return await lead_repo.get_by_status(db, status=status, skip=skip, limit=limit)
    return await lead_repo.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=LeadSchema, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_in: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new lead."""
    existing = await lead_repo.get_by_email(db, email=lead_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A lead with this email already exists",
        )
    return await lead_repo.create(db, obj_in=lead_in)


@router.get("/{lead_id}", response_model=LeadSchema)
async def read_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific lead by ID."""
    lead = await lead_repo.get(db, id=lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
    return lead


@router.put("/{lead_id}", response_model=LeadSchema)
async def update_lead(
    lead_id: int,
    lead_in: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an existing lead."""
    lead = await lead_repo.get(db, id=lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
    return await lead_repo.update(db, db_obj=lead, obj_in=lead_in)


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a lead."""
    lead = await lead_repo.get(db, id=lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
    await lead_repo.remove(db, id=lead_id)


@router.post("/{lead_id}/assign/{agent_id}", response_model=LeadSchema)
async def assign_lead_to_agent(
    lead_id: int,
    agent_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Assign a lead to an agent."""
    lead = await lead_repo.assign_agent(db, lead_id=lead_id, agent_id=agent_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
    return lead


@router.patch("/{lead_id}/status", response_model=LeadSchema)
async def update_lead_status(
    lead_id: int,
    new_status: LeadStatus = Query(..., alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update the status of a lead."""
    lead = await lead_repo.update_status(db, lead_id=lead_id, status=new_status)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
    return lead

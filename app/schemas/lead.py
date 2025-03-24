from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
from app.models.lead import LeadStatus
from .base import BaseSchema

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    source: str
    preferences: Dict = {}
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    assigned_agent_id: Optional[int] = None

class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[LeadStatus] = None
    preferences: Optional[Dict] = None
    notes: Optional[str] = None
    assigned_agent_id: Optional[int] = None

class LeadInDB(LeadBase, BaseSchema):
    status: LeadStatus
    assigned_agent_id: Optional[int]

class Lead(LeadInDB):
    pass

class LeadWithStats(Lead):
    appointments_count: int = 0
    last_appointment: Optional[str] = None
    next_appointment: Optional[str] = None 
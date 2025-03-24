from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.appointment import AppointmentStatus
from .base import BaseSchema

class AppointmentBase(BaseModel):
    scheduled_time: datetime
    notes: Optional[str] = None
    property_id: int
    lead_id: int
    agent_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    property_id: Optional[int] = None
    lead_id: Optional[int] = None
    agent_id: Optional[int] = None

class AppointmentInDB(AppointmentBase, BaseSchema):
    status: AppointmentStatus
    calendly_event_id: Optional[str] = None

class Appointment(AppointmentInDB):
    pass

class AppointmentWithDetails(Appointment):
    property_title: str
    lead_name: str
    agent_name: str 
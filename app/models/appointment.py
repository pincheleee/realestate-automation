from sqlalchemy import Column, DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class Appointment(BaseModel):
    __tablename__ = "appointments"
    
    scheduled_time = Column(DateTime, index=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    notes = Column(String)
    calendly_event_id = Column(String, unique=True)
    
    # Relationships
    property_id = Column(Integer, ForeignKey("properties.id"))
    property = relationship("Property", back_populates="appointments")
    lead_id = Column(Integer, ForeignKey("leads.id"))
    lead = relationship("Lead", back_populates="appointments")
    agent_id = Column(Integer, ForeignKey("users.id"))
    agent = relationship("User", back_populates="appointments") 
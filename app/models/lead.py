from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    NEGOTIATING = "negotiating"
    CLOSED = "closed"
    LOST = "lost"

class Lead(BaseModel):
    __tablename__ = "leads"
    
    name = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    source = Column(String)  # Where the lead came from
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    preferences = Column(JSON)  # Property preferences
    notes = Column(String)
    
    # Relationships
    assigned_agent_id = Column(Integer, ForeignKey("users.id"))
    assigned_agent = relationship("User", back_populates="leads")
    appointments = relationship("Appointment", back_populates="lead") 
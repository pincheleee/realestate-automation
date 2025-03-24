from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Property(BaseModel):
    __tablename__ = "properties"
    
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float, index=True)
    location = Column(String, index=True)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    square_feet = Column(Float)
    available = Column(Boolean, default=True)
    property_type = Column(String)
    listing_type = Column(String)
    features = Column(JSON)
    images = Column(JSON)  # List of image URLs
    mls_id = Column(String, unique=True, index=True)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="property")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="properties") 
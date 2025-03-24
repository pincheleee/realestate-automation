from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from .base import BaseSchema

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    location: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[float] = None
    property_type: str
    listing_type: str
    features: Dict = Field(default_factory=dict)
    images: List[str] = Field(default_factory=list)
    mls_id: Optional[str] = None

class PropertyCreate(PropertyBase):
    owner_id: int

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[float] = None
    available: Optional[bool] = None
    property_type: Optional[str] = None
    listing_type: Optional[str] = None
    features: Optional[Dict] = None
    images: Optional[List[str]] = None

class PropertyInDB(PropertyBase, BaseSchema):
    available: bool
    owner_id: int

class Property(PropertyInDB):
    pass

class PropertyWithStats(Property):
    views_count: int = 0
    appointments_count: int = 0
    leads_count: int = 0 
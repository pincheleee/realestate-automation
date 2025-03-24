from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime
from api.routes import router

from config import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Real Estate Automation System",
    description="API for automating real estate processes",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Data models
class Property(BaseModel):
    id: str
    title: str
    description: str
    price: float
    location: str
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    square_feet: Optional[float]
    available: bool

class Lead(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    preferences: dict
    created_at: datetime
    status: str

class Appointment(BaseModel):
    id: str
    lead_id: str
    property_id: str
    scheduled_time: datetime
    status: str

@app.get("/")
async def root():
    return {"message": "Real Estate Automation System API"}

@app.get("/properties")
async def get_properties():
    """Get all available properties"""
    try:
        # TODO: Implement property fetching from MLS
        return {"message": "Properties endpoint"}
    except Exception as e:
        logger.error(f"Error fetching properties: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching properties")

@app.post("/properties/facebook")
async def post_to_facebook(property_id: str):
    """Post a property to Facebook Marketplace"""
    try:
        # TODO: Implement Facebook Marketplace posting
        return {"message": "Property posted to Facebook"}
    except Exception as e:
        logger.error(f"Error posting to Facebook: {str(e)}")
        raise HTTPException(status_code=500, detail="Error posting to Facebook")

@app.post("/leads")
async def create_lead(lead: Lead):
    """Create a new lead"""
    try:
        # TODO: Implement lead creation and storage
        return {"message": "Lead created successfully"}
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating lead")

@app.post("/appointments")
async def schedule_appointment(appointment: Appointment):
    """Schedule a property showing"""
    try:
        # TODO: Implement Calendly integration
        return {"message": "Appointment scheduled successfully"}
    except Exception as e:
        logger.error(f"Error scheduling appointment: {str(e)}")
        raise HTTPException(status_code=500, detail="Error scheduling appointment")

@app.get("/recommendations/{lead_id}")
async def get_recommendations(lead_id: str):
    """Get personalized property recommendations for a lead"""
    try:
        # TODO: Implement recommendation engine
        return {"message": "Recommendations endpoint"}
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating recommendations")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
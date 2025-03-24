from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from datetime import datetime
from ..automation.main import RealEstateAutomation

router = APIRouter()
automation = RealEstateAutomation()

@router.post("/properties")
async def add_property(property_data: Dict):
    """Add a new property and process it through the automation system"""
    try:
        result = await automation.process_new_property(property_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/leads")
async def add_lead(lead_data: Dict):
    """Add a new lead and process it through the automation system"""
    try:
        result = await automation.process_new_lead(lead_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/appointments")
async def schedule_appointment(appointment_data: Dict):
    """Schedule a property showing"""
    try:
        result = await automation.schedule_property_showing(appointment_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = {
            "total_properties": len(automation.lead_manager.properties),
            "total_leads": len(automation.lead_manager.leads),
            "active_leads": len([l for l in automation.lead_manager.leads if l["status"] == "new"]),
            "scheduled_showings": len([l for l in automation.lead_manager.leads if l["status"] == "scheduled_showing"]),
            "recent_activities": []  # TODO: Implement activity tracking
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
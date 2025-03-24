import asyncio
import logging
from datetime import datetime
from typing import Dict, List

from .facebook_marketplace import FacebookMarketplaceBot
from .calendly_scheduler import CalendlyScheduler
from .lead_manager import LeadManager
from .gpt_assistant import GPTAssistant
from config import settings

logger = logging.getLogger(__name__)

class RealEstateAutomation:
    def __init__(self):
        self.facebook_bot = FacebookMarketplaceBot()
        self.calendly_scheduler = CalendlyScheduler()
        self.lead_manager = LeadManager()
        self.gpt_assistant = GPTAssistant()

    async def process_new_property(self, property_data: Dict) -> Dict:
        """
        Process a new property listing
        """
        try:
            # Enhance property description using GPT
            enhanced_description = await self.gpt_assistant.enhance_property_description(property_data)
            property_data['description'] = enhanced_description
            
            # Post to Facebook Marketplace
            fb_result = await self.facebook_bot.post_property(property_data)
            
            # Update property vectors for recommendations
            self.lead_manager.update_property_vectors([property_data])
            
            # Generate personalized responses for matching leads
            matching_leads = await self._find_matching_leads(property_data)
            for lead in matching_leads:
                await self._send_property_match_notification(lead, property_data)
            
            return {
                "status": "success",
                "facebook_post": fb_result,
                "property_id": property_data["id"],
                "enhanced_description": enhanced_description
            }
            
        except Exception as e:
            logger.error(f"Error processing new property: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def process_new_lead(self, lead_data: Dict) -> Dict:
        """
        Process a new lead
        """
        try:
            # Add lead to system
            lead_result = await self.lead_manager.add_lead(lead_data)
            
            if lead_result["status"] == "success":
                # Generate personalized welcome message
                welcome_message = await self.gpt_assistant.generate_lead_response(lead_data)
                
                # Get recommendations for the lead
                recommendations = lead_result["recommendations"]
                
                # Analyze matches with GPT
                match_analysis = []
                for property in recommendations:
                    analysis = await self.gpt_assistant.analyze_property_match(lead_data, property)
                    match_analysis.append(analysis)
                
                # Sort recommendations by match score
                recommendations.sort(key=lambda x: next(
                    (a["match_score"] for a in match_analysis if a["property_id"] == x["id"]), 0
                ), reverse=True)
                
                # Schedule initial consultation if needed
                if lead_data.get("schedule_consultation", False):
                    await self.calendly_scheduler.schedule_appointment({
                        "lead_id": lead_result["lead_id"],
                        "lead_name": lead_data["name"],
                        "lead_email": lead_data["email"],
                        "scheduled_time": datetime.now(),
                        "property_address": "Office Location"  # Replace with actual office location
                    })
                
                return {
                    "status": "success",
                    "lead_id": lead_result["lead_id"],
                    "welcome_message": welcome_message,
                    "recommendations": recommendations,
                    "match_analysis": match_analysis
                }
            
            return lead_result
            
        except Exception as e:
            logger.error(f"Error processing new lead: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def schedule_property_showing(self, appointment_data: Dict) -> Dict:
        """
        Schedule a property showing
        """
        try:
            # Generate personalized showing confirmation message
            lead_data = next((l for l in self.lead_manager.leads if l["id"] == appointment_data["lead_id"]), None)
            if lead_data:
                confirmation_message = await self.gpt_assistant.generate_lead_response(
                    lead_data,
                    {"title": appointment_data.get("property_title", ""), "location": appointment_data["property_address"]}
                )
                appointment_data["confirmation_message"] = confirmation_message
            
            # Schedule through Calendly
            result = await self.calendly_scheduler.schedule_appointment(appointment_data)
            
            if result["status"] == "success":
                # Update lead status
                await self.lead_manager.update_lead_status(
                    appointment_data["lead_id"],
                    "scheduled_showing"
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error scheduling property showing: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _find_matching_leads(self, property_data: Dict) -> List[Dict]:
        """
        Find leads that might be interested in the property
        """
        matching_leads = []
        for lead in self.lead_manager.leads:
            analysis = await self.gpt_assistant.analyze_property_match(lead, property_data)
            if analysis["match_score"] >= 70:  # Consider leads with match score >= 70
                matching_leads.append(lead)
        return matching_leads

    async def _send_property_match_notification(self, lead: Dict, property_data: Dict) -> None:
        """
        Send notification to lead about matching property
        """
        try:
            # Generate personalized message
            message = await self.gpt_assistant.generate_lead_response(lead, property_data)
            
            # TODO: Implement actual notification sending (email, SMS, etc.)
            logger.info(f"Would send notification to lead {lead['id']} about property {property_data['id']}")
            
        except Exception as e:
            logger.error(f"Error sending property match notification: {str(e)}")

# Example usage
async def main():
    automation = RealEstateAutomation()
    
    # Example property data
    property_data = {
        "id": "1",
        "title": "Beautiful 3 Bedroom Home",
        "description": "Modern home with updated features",
        "price": 350000,
        "location": "San Francisco, CA",
        "bedrooms": 3,
        "bathrooms": 2,
        "square_feet": 1500
    }
    
    # Process new property
    result = await automation.process_new_property(property_data)
    print(f"Property processing result: {result}")
    
    # Example lead data
    lead_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-0123",
        "preferences": {
            "location": "San Francisco",
            "price_range": "300000-400000",
            "features": "3 bedrooms, modern kitchen"
        },
        "schedule_consultation": True
    }
    
    # Process new lead
    result = await automation.process_new_lead(lead_data)
    print(f"Lead processing result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 
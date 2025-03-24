import aiohttp
from typing import Dict, List
import logging
from datetime import datetime, timedelta
from config import settings

logger = logging.getLogger(__name__)

class CalendlyScheduler:
    def __init__(self):
        self.api_key = settings.CALENDLY_API_KEY
        self.base_url = settings.CALENDLY_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def schedule_appointment(self, appointment_data: Dict) -> Dict:
        """
        Schedule a property showing through Calendly
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Create scheduling link
                scheduling_link = await self._create_scheduling_link(session, appointment_data)
                
                # Send scheduling link to lead
                await self._send_scheduling_link(appointment_data["lead_email"], scheduling_link)
                
                logger.info(f"Successfully scheduled appointment for lead {appointment_data['lead_id']}")
                return {
                    "status": "success",
                    "scheduling_link": scheduling_link
                }
                
        except Exception as e:
            logger.error(f"Error scheduling appointment: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _create_scheduling_link(self, session: aiohttp.ClientSession, appointment_data: Dict) -> str:
        """
        Create a scheduling link for the appointment
        """
        payload = {
            "start_time": appointment_data["scheduled_time"].isoformat(),
            "end_time": (appointment_data["scheduled_time"] + timedelta(hours=1)).isoformat(),
            "event_type": "property_showing",
            "location": appointment_data["property_address"],
            "invitees": [{
                "email": appointment_data["lead_email"],
                "name": appointment_data["lead_name"]
            }]
        }
        
        async with session.post(
            f"{self.base_url}/scheduling_links",
            headers=self.headers,
            json=payload
        ) as response:
            data = await response.json()
            return data["booking_url"]

    async def _send_scheduling_link(self, email: str, scheduling_link: str) -> None:
        """
        Send the scheduling link to the lead
        """
        # Implement email sending logic here
        # You can use your preferred email service (SendGrid, AWS SES, etc.)
        pass 
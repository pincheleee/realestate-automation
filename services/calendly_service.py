import aiohttp
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from config import settings

logger = logging.getLogger(__name__)

class CalendlyService:
    def __init__(self):
        self.api_key = settings.CALENDLY_API_KEY
        self.base_url = settings.CALENDLY_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_available_times(self, 
                                start_time: datetime,
                                end_time: datetime,
                                event_type: str = "property-viewing") -> List[Dict[str, Any]]:
        """
        Get available time slots for property viewings
        
        Args:
            start_time: Start of the time range to check
            end_time: End of the time range to check
            event_type: Type of event to schedule
            
        Returns:
            List of available time slots
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "event_type": event_type
                }
                
                async with session.get(
                    f"{self.base_url}/scheduled_events/available_times",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("available_times", [])
                    else:
                        logger.error(f"Error getting available times: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching available times: {str(e)}")
            return []

    async def schedule_appointment(self,
                                 email: str,
                                 start_time: datetime,
                                 event_type: str = "property-viewing",
                                 custom_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Schedule a property viewing appointment
        
        Args:
            email: Email address of the person scheduling
            start_time: Desired start time of the appointment
            event_type: Type of event to schedule
            custom_data: Additional data to include with the appointment
            
        Returns:
            Dict containing the scheduled appointment details
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "start_time": start_time.isoformat(),
                    "event_type": event_type,
                    "email": email,
                    "custom_data": custom_data or {}
                }
                
                async with session.post(
                    f"{self.base_url}/scheduled_events",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 201:
                        return await response.json()
                    else:
                        logger.error(f"Error scheduling appointment: {response.status}")
                        raise Exception("Failed to schedule appointment")
                        
        except Exception as e:
            logger.error(f"Error scheduling appointment: {str(e)}")
            raise

    async def cancel_appointment(self, event_uuid: str) -> bool:
        """
        Cancel a scheduled appointment
        
        Args:
            event_uuid: UUID of the event to cancel
            
        Returns:
            bool: True if cancellation was successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.base_url}/scheduled_events/{event_uuid}",
                    headers=self.headers
                ) as response:
                    if response.status == 204:
                        return True
                    else:
                        logger.error(f"Error canceling appointment: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error canceling appointment: {str(e)}")
            return False

    async def get_appointment_details(self, event_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a scheduled appointment
        
        Args:
            event_uuid: UUID of the event to get details for
            
        Returns:
            Dict containing appointment details or None if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/scheduled_events/{event_uuid}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error getting appointment details: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching appointment details: {str(e)}")
            return None

    async def send_reminder(self, event_uuid: str, reminder_type: str = "email") -> bool:
        """
        Send a reminder for an upcoming appointment
        
        Args:
            event_uuid: UUID of the event to send reminder for
            reminder_type: Type of reminder to send (email, sms, etc.)
            
        Returns:
            bool: True if reminder was sent successfully
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "reminder_type": reminder_type
                }
                
                async with session.post(
                    f"{self.base_url}/scheduled_events/{event_uuid}/reminder",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"Error sending reminder: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending reminder: {str(e)}")
            return False 
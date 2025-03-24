import aiohttp
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from config import settings

logger = logging.getLogger(__name__)

class FollowUpService:
    def __init__(self):
        self.api_key = settings.FOLLOWUPBOSS_API_KEY
        self.base_url = settings.FOLLOWUPBOSS_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def create_lead(self, lead_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new lead in FollowUpBoss
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dict containing created lead details or None if failed
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/leads",
                    headers=self.headers,
                    json=lead_data
                ) as response:
                    if response.status == 201:
                        return await response.json()
                    else:
                        logger.error(f"Error creating lead: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error creating lead: {str(e)}")
            return None

    async def get_lead_details(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific lead
        
        Args:
            lead_id: ID of the lead to get details for
            
        Returns:
            Dict containing lead details or None if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/leads/{lead_id}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching lead details: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching lead details: {str(e)}")
            return None

    async def update_lead_status(self,
                               lead_id: str,
                               status: str,
                               notes: Optional[str] = None) -> bool:
        """
        Update the status of a lead
        
        Args:
            lead_id: ID of the lead to update
            status: New status to set
            notes: Optional notes about the status change
            
        Returns:
            bool: True if update was successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "status": status,
                    "notes": notes
                }
                
                async with session.patch(
                    f"{self.base_url}/leads/{lead_id}",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"Error updating lead status: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error updating lead status: {str(e)}")
            return False

    async def schedule_follow_up(self,
                               lead_id: str,
                               follow_up_time: datetime,
                               follow_up_type: str = "email",
                               notes: Optional[str] = None) -> bool:
        """
        Schedule a follow-up for a lead
        
        Args:
            lead_id: ID of the lead to schedule follow-up for
            follow_up_time: When to follow up
            follow_up_type: Type of follow-up (email, call, etc.)
            notes: Optional notes about the follow-up
            
        Returns:
            bool: True if scheduling was successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "lead_id": lead_id,
                    "scheduled_time": follow_up_time.isoformat(),
                    "type": follow_up_type,
                    "notes": notes
                }
                
                async with session.post(
                    f"{self.base_url}/follow-ups",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 201:
                        return True
                    else:
                        logger.error(f"Error scheduling follow-up: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error scheduling follow-up: {str(e)}")
            return False

    async def get_lead_activity(self, lead_id: str) -> List[Dict[str, Any]]:
        """
        Get the activity history of a lead
        
        Args:
            lead_id: ID of the lead to get activity for
            
        Returns:
            List of activity events
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/leads/{lead_id}/activity",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching lead activity: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching lead activity: {str(e)}")
            return []

    async def send_automated_message(self,
                                   lead_id: str,
                                   message: str,
                                   message_type: str = "email") -> bool:
        """
        Send an automated message to a lead
        
        Args:
            lead_id: ID of the lead to send message to
            message: Content of the message
            message_type: Type of message (email, sms, etc.)
            
        Returns:
            bool: True if message was sent successfully
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "lead_id": lead_id,
                    "message": message,
                    "type": message_type
                }
                
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 201:
                        return True
                    else:
                        logger.error(f"Error sending message: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False

    async def get_leads_needing_follow_up(self) -> List[Dict[str, Any]]:
        """
        Get leads that need follow-up based on their status and last activity
        
        Returns:
            List of leads needing follow-up
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "status": "active",
                    "last_activity_before": (datetime.now() - timedelta(days=3)).isoformat()
                }
                
                async with session.get(
                    f"{self.base_url}/leads",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching leads needing follow-up: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching leads needing follow-up: {str(e)}")
            return [] 
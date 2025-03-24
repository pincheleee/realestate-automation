import aiohttp
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

class MLSService:
    def __init__(self):
        self.api_key = settings.MLS_API_KEY
        self.base_url = settings.MLS_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_properties(self,
                           filters: Optional[Dict[str, Any]] = None,
                           page: int = 1,
                           page_size: int = 20) -> Dict[str, Any]:
        """
        Get properties from MLS database
        
        Args:
            filters: Dictionary of filters to apply
            page: Page number for pagination
            page_size: Number of items per page
            
        Returns:
            Dict containing properties and pagination info
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "page": page,
                    "page_size": page_size,
                    **(filters or {})
                }
                
                async with session.get(
                    f"{self.base_url}/properties",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching properties: {response.status}")
                        return {"properties": [], "total": 0, "page": page, "page_size": page_size}
                        
        except Exception as e:
            logger.error(f"Error fetching properties: {str(e)}")
            return {"properties": [], "total": 0, "page": page, "page_size": page_size}

    async def get_property_details(self, property_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific property
        
        Args:
            property_id: ID of the property to get details for
            
        Returns:
            Dict containing property details or None if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/properties/{property_id}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching property details: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching property details: {str(e)}")
            return None

    async def check_availability(self, property_id: str) -> bool:
        """
        Check if a property is currently available
        
        Args:
            property_id: ID of the property to check
            
        Returns:
            bool: True if property is available
        """
        try:
            property_details = await self.get_property_details(property_id)
            if property_details:
                return property_details.get("status", "").lower() == "available"
            return False
            
        except Exception as e:
            logger.error(f"Error checking property availability: {str(e)}")
            return False

    async def get_similar_properties(self,
                                   property_id: str,
                                   limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get similar properties based on a reference property
        
        Args:
            property_id: ID of the reference property
            limit: Maximum number of similar properties to return
            
        Returns:
            List of similar properties
        """
        try:
            property_details = await self.get_property_details(property_id)
            if not property_details:
                return []
                
            # Extract relevant features for comparison
            features = {
                "price_range": {
                    "min": property_details["price"] * 0.8,
                    "max": property_details["price"] * 1.2
                },
                "location": property_details["location"],
                "property_type": property_details["property_type"],
                "bedrooms": property_details["bedrooms"]
            }
            
            # Search for similar properties
            filters = {
                "price_min": features["price_range"]["min"],
                "price_max": features["price_range"]["max"],
                "property_type": features["property_type"],
                "bedrooms": features["bedrooms"]
            }
            
            results = await self.get_properties(filters=filters, page_size=limit)
            return results.get("properties", [])
            
        except Exception as e:
            logger.error(f"Error finding similar properties: {str(e)}")
            return []

    async def update_property_status(self,
                                   property_id: str,
                                   status: str,
                                   additional_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update the status of a property
        
        Args:
            property_id: ID of the property to update
            status: New status to set
            additional_info: Additional information to update
            
        Returns:
            bool: True if update was successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "status": status,
                    **(additional_info or {})
                }
                
                async with session.patch(
                    f"{self.base_url}/properties/{property_id}",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"Error updating property status: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error updating property status: {str(e)}")
            return False

    async def get_property_history(self, property_id: str) -> List[Dict[str, Any]]:
        """
        Get the history of a property (price changes, status updates, etc.)
        
        Args:
            property_id: ID of the property to get history for
            
        Returns:
            List of historical events
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/properties/{property_id}/history",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching property history: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching property history: {str(e)}")
            return [] 
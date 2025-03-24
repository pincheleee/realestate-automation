import facebook
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

class FacebookService:
    def __init__(self):
        self.graph = facebook.GraphAPI(
            access_token=settings.FACEBOOK_APP_SECRET,
            version=settings.FACEBOOK_API_VERSION
        )
        
    async def post_to_marketplace(self, property_data: Dict[str, Any]) -> str:
        """
        Post a property listing to Facebook Marketplace
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            str: The ID of the created marketplace listing
        """
        try:
            # Format the listing data according to Facebook's requirements
            listing_data = {
                "title": property_data["title"],
                "description": property_data["description"],
                "price": property_data["price"],
                "category": "RENTAL",
                "location": {
                    "latitude": property_data.get("latitude"),
                    "longitude": property_data.get("longitude"),
                    "city": property_data.get("city"),
                    "state": property_data.get("state"),
                    "zip": property_data.get("zip")
                },
                "images": property_data.get("images", []),
                "availability": "AVAILABLE" if property_data.get("available", True) else "SOLD"
            }
            
            # Create the marketplace listing
            response = self.graph.put_object(
                parent_object="me",
                connection_name="marketplace_listings",
                **listing_data
            )
            
            logger.info(f"Successfully posted property to Facebook Marketplace: {response['id']}")
            return response["id"]
            
        except facebook.GraphAPIError as e:
            logger.error(f"Facebook API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error posting to Facebook Marketplace: {str(e)}")
            raise

    async def handle_messenger_message(self, sender_id: str, message: str) -> Dict[str, Any]:
        """
        Handle incoming Messenger messages and respond appropriately
        
        Args:
            sender_id: The ID of the message sender
            message: The message content
            
        Returns:
            Dict containing the response data
        """
        try:
            # Basic message handling logic
            if "schedule" in message.lower() or "appointment" in message.lower():
                return {
                    "type": "scheduling",
                    "message": "I can help you schedule a property viewing. Would you like to see our available times?",
                    "quick_replies": [
                        {"title": "Yes, show me times", "payload": "SHOW_TIMES"},
                        {"title": "No, thanks", "payload": "DECLINE"}
                    ]
                }
            elif "price" in message.lower() or "cost" in message.lower():
                return {
                    "type": "price_info",
                    "message": "I can help you with pricing information. What type of property are you interested in?",
                    "quick_replies": [
                        {"title": "House", "payload": "HOUSE"},
                        {"title": "Apartment", "payload": "APARTMENT"}
                    ]
                }
            else:
                return {
                    "type": "general",
                    "message": "I'm here to help you with your real estate needs. What would you like to know?",
                    "quick_replies": [
                        {"title": "View Properties", "payload": "VIEW_PROPERTIES"},
                        {"title": "Schedule Viewing", "payload": "SCHEDULE"},
                        {"title": "Contact Agent", "payload": "CONTACT"}
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error handling Messenger message: {str(e)}")
            return {
                "type": "error",
                "message": "I apologize, but I'm having trouble processing your request. Please try again later."
            }

    async def collect_lead_info(self, sender_id: str, step: str, user_input: str) -> Dict[str, Any]:
        """
        Collect lead information through a conversational flow
        
        Args:
            sender_id: The ID of the message sender
            step: The current step in the lead collection process
            user_input: The user's input for the current step
            
        Returns:
            Dict containing the next step and response
        """
        try:
            # Store user input in a temporary storage (implement your own storage solution)
            # This is a simplified example
            lead_data = {}
            
            if step == "name":
                lead_data["name"] = user_input
                return {
                    "next_step": "email",
                    "message": "Great! What's your email address?"
                }
            elif step == "email":
                lead_data["email"] = user_input
                return {
                    "next_step": "phone",
                    "message": "Thanks! What's your phone number?"
                }
            elif step == "phone":
                lead_data["phone"] = user_input
                return {
                    "next_step": "preferences",
                    "message": "What type of property are you looking for?",
                    "quick_replies": [
                        {"title": "House", "payload": "HOUSE"},
                        {"title": "Apartment", "payload": "APARTMENT"},
                        {"title": "Condo", "payload": "CONDO"}
                    ]
                }
            elif step == "preferences":
                lead_data["property_type"] = user_input
                # Save the complete lead data
                # await save_lead_data(sender_id, lead_data)
                return {
                    "next_step": "complete",
                    "message": "Thank you for providing your information! An agent will contact you soon."
                }
                
        except Exception as e:
            logger.error(f"Error collecting lead information: {str(e)}")
            return {
                "next_step": "error",
                "message": "I apologize, but I'm having trouble processing your information. Please try again later."
            } 
import facebook
from typing import Dict, List
import logging
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

class FacebookMarketplaceBot:
    def __init__(self):
        self.graph = facebook.GraphAPI(access_token=settings.FACEBOOK_APP_SECRET)
        self.api_version = settings.FACEBOOK_API_VERSION

    async def post_property(self, property_data: Dict) -> Dict:
        """
        Post a property to Facebook Marketplace
        """
        try:
            # Format property data for Facebook
            post_data = {
                "message": f"{property_data['title']}\n\n{property_data['description']}\n\nPrice: ${property_data['price']:,}",
                "attached_media": [],  # Add property images here
                "targeting": {
                    "geo_locations": {
                        "countries": ["US"],
                        "regions": [{"key": property_data['location']}]
                    }
                }
            }
            
            # Post to Facebook Marketplace
            response = self.graph.put_object(
                parent_object="me",
                connection_name="feed",
                **post_data
            )
            
            logger.info(f"Successfully posted property {property_data['id']} to Facebook Marketplace")
            return {"status": "success", "post_id": response["id"]}
            
        except Exception as e:
            logger.error(f"Error posting to Facebook Marketplace: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def get_marketplace_listings(self) -> List[Dict]:
        """
        Get current marketplace listings
        """
        try:
            response = self.graph.get_connections(
                "me",
                "feed",
                fields="message,created_time,attachments"
            )
            return response["data"]
        except Exception as e:
            logger.error(f"Error fetching marketplace listings: {str(e)}")
            return [] 
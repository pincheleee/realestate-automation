import logging
from typing import Dict, List
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class LeadManager:
    def __init__(self):
        self.leads = []
        self.vectorizer = TfidfVectorizer()
        self.property_vectors = None
        self.properties = []

    async def add_lead(self, lead_data: Dict) -> Dict:
        """
        Add a new lead to the system
        """
        try:
            lead = {
                "id": str(len(self.leads) + 1),
                "created_at": datetime.now(),
                "status": "new",
                **lead_data
            }
            self.leads.append(lead)
            
            # Generate recommendations for the new lead
            recommendations = await self.get_recommendations(lead["id"])
            
            logger.info(f"Successfully added lead {lead['id']}")
            return {
                "status": "success",
                "lead_id": lead["id"],
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error adding lead: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def update_lead_status(self, lead_id: str, new_status: str) -> Dict:
        """
        Update the status of a lead
        """
        try:
            lead = next((l for l in self.leads if l["id"] == lead_id), None)
            if lead:
                lead["status"] = new_status
                return {"status": "success", "message": "Lead status updated"}
            return {"status": "error", "message": "Lead not found"}
        except Exception as e:
            logger.error(f"Error updating lead status: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def get_recommendations(self, lead_id: str) -> List[Dict]:
        """
        Get personalized property recommendations for a lead
        """
        try:
            lead = next((l for l in self.leads if l["id"] == lead_id), None)
            if not lead:
                return []

            # Convert lead preferences to text for vectorization
            preferences_text = f"{lead['preferences'].get('location', '')} {lead['preferences'].get('price_range', '')} {lead['preferences'].get('features', '')}"
            
            # Vectorize preferences
            lead_vector = self.vectorizer.transform([preferences_text])
            
            # Calculate similarity scores
            similarity_scores = cosine_similarity(lead_vector, self.property_vectors).flatten()
            
            # Get top 5 recommendations
            top_indices = similarity_scores.argsort()[-5:][::-1]
            recommendations = [self.properties[i] for i in top_indices]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []

    def update_property_vectors(self, properties: List[Dict]):
        """
        Update property vectors for recommendation system
        """
        self.properties = properties
        property_texts = [
            f"{p['location']} {p['price']} {p['description']}"
            for p in properties
        ]
        self.property_vectors = self.vectorizer.fit_transform(property_texts) 
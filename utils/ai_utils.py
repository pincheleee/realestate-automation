from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class PropertyRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.property_vectors = None
        self.properties = []

    def train(self, properties: List[Dict[str, Any]]):
        """
        Train the recommender system with property data
        
        Args:
            properties: List of property dictionaries
        """
        try:
            self.properties = properties
            # Create property descriptions for vectorization
            descriptions = [
                f"{p.get('title', '')} {p.get('description', '')} "
                f"{p.get('property_type', '')} {p.get('location', '')} "
                f"{p.get('features', [])}"
                for p in properties
            ]
            
            # Create TF-IDF vectors
            self.property_vectors = self.vectorizer.fit_transform(descriptions)
            
        except Exception as e:
            logger.error(f"Error training recommender: {str(e)}")
            raise

    def get_recommendations(self,
                          preferences: Dict[str, Any],
                          n_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Get property recommendations based on preferences
        
        Args:
            preferences: Dictionary of user preferences
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended properties
        """
        try:
            if not self.property_vectors or not self.properties:
                return []

            # Create preference description
            pref_description = (
                f"{preferences.get('property_type', '')} "
                f"{preferences.get('location', '')} "
                f"{preferences.get('features', [])}"
            )

            # Vectorize preferences
            pref_vector = self.vectorizer.transform([pref_description])

            # Calculate similarities
            similarities = cosine_similarity(pref_vector, self.property_vectors).flatten()

            # Get top recommendations
            top_indices = np.argsort(similarities)[-n_recommendations:][::-1]
            recommendations = [self.properties[i] for i in top_indices]

            return recommendations

        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return []

class LeadScorer:
    def __init__(self):
        self.weights = {
            "response_time": 0.3,
            "engagement_level": 0.2,
            "property_interest": 0.2,
            "budget_alignment": 0.15,
            "timeline": 0.15
        }

    def score_lead(self, lead_data: Dict[str, Any]) -> float:
        """
        Score a lead based on various factors
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            float: Lead score between 0 and 1
        """
        try:
            scores = {
                "response_time": self._score_response_time(lead_data),
                "engagement_level": self._score_engagement(lead_data),
                "property_interest": self._score_property_interest(lead_data),
                "budget_alignment": self._score_budget_alignment(lead_data),
                "timeline": self._score_timeline(lead_data)
            }

            # Calculate weighted average
            total_score = sum(
                score * self.weights[factor]
                for factor, score in scores.items()
            )

            return min(max(total_score, 0), 1)  # Ensure score is between 0 and 1

        except Exception as e:
            logger.error(f"Error scoring lead: {str(e)}")
            return 0.0

    def _score_response_time(self, lead_data: Dict[str, Any]) -> float:
        """Score based on how quickly the lead responds"""
        try:
            response_times = lead_data.get("response_times", [])
            if not response_times:
                return 0.5

            avg_response_time = sum(response_times) / len(response_times)
            # Convert to score (lower response time = higher score)
            return 1 / (1 + avg_response_time)

        except Exception as e:
            logger.error(f"Error scoring response time: {str(e)}")
            return 0.5

    def _score_engagement(self, lead_data: Dict[str, Any]) -> float:
        """Score based on lead engagement level"""
        try:
            activities = lead_data.get("activities", [])
            if not activities:
                return 0.5

            # Count different types of activities
            activity_types = set(activity["type"] for activity in activities)
            return min(len(activity_types) / 5, 1)  # Normalize to 0-1

        except Exception as e:
            logger.error(f"Error scoring engagement: {str(e)}")
            return 0.5

    def _score_property_interest(self, lead_data: Dict[str, Any]) -> float:
        """Score based on property interest level"""
        try:
            viewed_properties = lead_data.get("viewed_properties", [])
            if not viewed_properties:
                return 0.5

            # Consider number of properties viewed and time spent
            total_time = sum(prop.get("view_time", 0) for prop in viewed_properties)
            return min((len(viewed_properties) * total_time) / 1000, 1)  # Normalize

        except Exception as e:
            logger.error(f"Error scoring property interest: {str(e)}")
            return 0.5

    def _score_budget_alignment(self, lead_data: Dict[str, Any]) -> float:
        """Score based on budget alignment with available properties"""
        try:
            lead_budget = lead_data.get("budget", 0)
            property_prices = lead_data.get("viewed_properties", [])
            
            if not property_prices:
                return 0.5

            avg_price = sum(prop.get("price", 0) for prop in property_prices) / len(property_prices)
            price_diff = abs(lead_budget - avg_price)
            
            # Score based on how close the budget is to average property price
            return 1 / (1 + price_diff / lead_budget)

        except Exception as e:
            logger.error(f"Error scoring budget alignment: {str(e)}")
            return 0.5

    def _score_timeline(self, lead_data: Dict[str, Any]) -> float:
        """Score based on the lead's timeline"""
        try:
            timeline = lead_data.get("timeline", "")
            urgency_keywords = ["immediate", "asap", "urgent", "now", "quick"]
            
            if not timeline:
                return 0.5

            # Score based on urgency keywords
            urgency_score = sum(1 for keyword in urgency_keywords if keyword in timeline.lower())
            return min(urgency_score / len(urgency_keywords), 1)

        except Exception as e:
            logger.error(f"Error scoring timeline: {str(e)}")
            return 0.5

class MessageGenerator:
    def __init__(self):
        self.templates = {
            "follow_up": [
                "Hi {name}, I noticed you were interested in {property_type} properties. "
                "I have some new listings that might match your criteria. Would you like to see them?",
                "Hello {name}, I wanted to follow up on your interest in {property_type} properties. "
                "I have some great options available now. Would you like to schedule a viewing?",
                "Hi {name}, I hope you're still looking for {property_type} properties. "
                "I have some new listings that could be perfect for you. Would you like to learn more?"
            ],
            "appointment_reminder": [
                "Hi {name}, this is a reminder about your property viewing tomorrow at {time}. "
                "The address is {address}. Looking forward to meeting you!",
                "Hello {name}, just confirming your appointment tomorrow at {time} to view "
                "the property at {address}. See you then!"
            ],
            "property_update": [
                "Hi {name}, I wanted to let you know that {property_title} is still available. "
                "Would you like to schedule a viewing?",
                "Hello {name}, {property_title} is still on the market. "
                "Would you like to see it in person?"
            ]
        }

    def generate_message(self,
                        message_type: str,
                        context: Dict[str, Any]) -> str:
        """
        Generate a personalized message based on type and context
        
        Args:
            message_type: Type of message to generate
            context: Dictionary containing context variables
            
        Returns:
            str: Generated message
        """
        try:
            if message_type not in self.templates:
                raise ValueError(f"Unknown message type: {message_type}")

            # Select a random template for the message type
            template = np.random.choice(self.templates[message_type])
            
            # Format the template with context
            return template.format(**context)

        except Exception as e:
            logger.error(f"Error generating message: {str(e)}")
            return "I apologize, but I'm having trouble generating a message. Please try again later." 
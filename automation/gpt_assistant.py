import openai
from typing import Dict, List, Optional
import logging
from config import settings

logger = logging.getLogger(__name__)

class GPTAssistant:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"

    async def enhance_property_description(self, property_data: Dict) -> str:
        """
        Enhance property description using GPT
        """
        try:
            prompt = f"""
            Create an engaging property description for a real estate listing with the following details:
            Title: {property_data['title']}
            Price: ${property_data['price']:,}
            Location: {property_data['location']}
            Bedrooms: {property_data.get('bedrooms', 'N/A')}
            Bathrooms: {property_data.get('bathrooms', 'N/A')}
            Square Feet: {property_data.get('square_feet', 'N/A')}
            Current Description: {property_data.get('description', '')}

            Create a compelling description that highlights the property's best features and appeals to potential buyers.
            Include details about the neighborhood, lifestyle benefits, and unique selling points.
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional real estate copywriter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error enhancing property description: {str(e)}")
            return property_data.get('description', '')

    async def generate_lead_response(self, lead_data: Dict, property_data: Optional[Dict] = None) -> str:
        """
        Generate personalized response for a lead
        """
        try:
            prompt = f"""
            Create a personalized response for a potential real estate client with the following details:
            Name: {lead_data['name']}
            Preferences: {lead_data['preferences']}
            Status: {lead_data.get('status', 'new')}
            """

            if property_data:
                prompt += f"""
                Property of Interest:
                Title: {property_data['title']}
                Price: ${property_data['price']:,}
                Location: {property_data['location']}
                """

            prompt += """
            Create a friendly, professional response that:
            1. Acknowledges their interest
            2. Addresses their specific preferences
            3. Offers to help them find the perfect property
            4. Includes a clear call to action
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional real estate agent assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating lead response: {str(e)}")
            return "Thank you for your interest. I'll be in touch shortly to help you find your perfect property."

    async def analyze_property_match(self, lead_data: Dict, property_data: Dict) -> Dict:
        """
        Analyze how well a property matches a lead's preferences using GPT
        """
        try:
            prompt = f"""
            Analyze how well this property matches the lead's preferences:

            Lead Preferences:
            {lead_data['preferences']}

            Property Details:
            Title: {property_data['title']}
            Price: ${property_data['price']:,}
            Location: {property_data['location']}
            Bedrooms: {property_data.get('bedrooms', 'N/A')}
            Bathrooms: {property_data.get('bathrooms', 'N/A')}
            Square Feet: {property_data.get('square_feet', 'N/A')}
            Description: {property_data.get('description', '')}

            Provide a detailed analysis including:
            1. Match score (0-100)
            2. Key matching features
            3. Potential concerns
            4. Recommendations for follow-up
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a real estate matchmaking expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            analysis = response.choices[0].message.content
            
            # Parse the analysis into structured data
            return {
                "match_score": self._extract_match_score(analysis),
                "analysis": analysis,
                "property_id": property_data["id"],
                "lead_id": lead_data["id"]
            }

        except Exception as e:
            logger.error(f"Error analyzing property match: {str(e)}")
            return {
                "match_score": 0,
                "analysis": "Error analyzing property match",
                "property_id": property_data["id"],
                "lead_id": lead_data["id"]
            }

    def _extract_match_score(self, analysis: str) -> int:
        """
        Extract match score from GPT analysis
        """
        try:
            # Look for a number between 0-100 in the analysis
            import re
            match = re.search(r'\b\d{1,3}\b', analysis)
            if match:
                score = int(match.group())
                return min(max(score, 0), 100)  # Ensure score is between 0-100
            return 50  # Default score if no number found
        except:
            return 50  # Default score if error occurs 
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class CopywritingService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def generate_copy(self, segment: str, product_name: str, product_description: str, brand_tone: str):
        prompt = f"""
        You are a world-class creative director at a top marketing agency.
        Generate a hyper-personalized marketing copy for a specific customer segment.
        
        Product: {product_name}
        Description: {product_description}
        Brand Tone: {brand_tone}
        Customer Segment: {segment}
        
        Context for Segments:
        - High-value loyalists: Reward their loyalty, use VIP language, exclusive feel.
        - Window shoppers: Drive urgency, highlight benefits, maybe a first-purchase incentive.
        - Lapsed customers: "We miss you" vibe, strong re-engagement offer (e.g., 20% off).
        
        Output format:
        Headline: [Punchy headline]
        Body: [Short, engaging copy - max 2 sentences]
        CTA: [Clear call to action]
        """
        
        if not self.client:
            # Fallback mock responses for development/no API key
            return self._get_mock_copy(segment, product_name)
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You generate high-converting marketing copy."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return self._get_mock_copy(segment, product_name)

    def _get_mock_copy(self, segment: str, product_name: str):
        if "loyalists" in segment.lower():
            return f"Headline: Exclusive VIP Access\nBody: As one of our most valued customers, we wanted you to be the first to see our new {product_name} collection.\nCTA: Shop the Collection"
        elif "lapsed" in segment.lower():
            return f"Headline: We Miss You!\nBody: It's been a while! Come back and enjoy 20% off your next {product_name} order.\nCTA: Claim My Discount"
        else:
            return f"Headline: Ready to Upgrade?\nBody: Discover why everyone is talking about {product_name}. Experience the difference today.\nCTA: Learn More"


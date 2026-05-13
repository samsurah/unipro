import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ImageGenService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def generate_image(self, segment: str, product_name: str, copy_vibe: str, brand_tone: str):
        # Construct a visual prompt based on the segment and product
        visual_context = ""
        if "loyalists" in segment.lower():
            visual_context = "premium setting, luxury lighting, cinematic, high-end feel"
        elif "lapsed" in segment.lower():
            visual_context = "warm, inviting, welcoming atmosphere, bright colors"
        else:
            visual_context = "clean, minimalist, modern lifestyle setting"

        image_prompt = f"Professional product photography of {product_name}. Style: {brand_tone}. Setting: {visual_context}. High resolution, 4k, marketing quality."
        
        if not self.client:
            # Fallback to a placeholder image
            return f"https://picsum.photos/seed/{product_name.replace(' ', '')}{segment[:3]}/1024/1024"
            
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            print(f"Error calling DALL-E: {e}")
            return f"https://picsum.photos/seed/{product_name.replace(' ', '')}/1024/1024"


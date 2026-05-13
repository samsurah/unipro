from pydantic import BaseModel
from typing import List, Optional

class ProductContext(BaseModel):
    product_name: str
    product_description: str
    brand_tone: str

class AdVariation(BaseModel):
    id: str
    segment: str
    copy: str
    image_url: str
    clicks: int = 0
    conversions: int = 0

class SimulationInput(BaseModel):
    ad_id: str
    action: str # "click" or "conversion"

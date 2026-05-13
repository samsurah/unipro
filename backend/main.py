from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Agency-in-a-Box API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Agency-in-a-Box API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from services.segmentation import SegmentationService
from services.copywriting import CopywritingService
from services.image_gen import ImageGenService
from services.optimization import MultiArmedBanditService
from models import ProductContext, SimulationInput
import pandas as pd
import io
import uuid
from typing import Dict, List

# In-memory store for demonstration
db = {
    "ads": [],
    "segments": {}
}

segmentation_service = SegmentationService()
copy_service = CopywritingService()
image_service = ImageGenService()

@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    rfm = segmentation_service.calculate_rfm(df)
    clustered = segmentation_service.cluster_customers(rfm)
    
    results = clustered['Segment'].value_counts().to_dict()
    db["segments"] = clustered.to_dict(orient="index")
    
    return {"message": "Data processed", "segments": results}

@app.get("/sample-data")
async def get_sample():
    df = segmentation_service.generate_sample_data(50)
    csv_string = df.to_csv(index=False)
    return {"csv": csv_string}

@app.post("/generate-ads")
async def generate_ads(context: ProductContext):
    segments = ["High-value loyalists", "Window shoppers", "Lapsed customers"]
    new_ads = []
    
    for segment in segments:
        copy = await copy_service.generate_copy(
            segment, context.product_name, context.product_description, context.brand_tone
        )
        image_url = await image_service.generate_image(
            segment, context.product_name, copy, context.brand_tone
        )
        
        ad = {
            "id": str(uuid.uuid4()),
            "segment": segment,
            "copy": copy,
            "image_url": image_url,
            "clicks": 0,
            "impressions": 100, # Initial seed
            "product_name": context.product_name
        }
        new_ads.append(ad)
    
    db["ads"] = new_ads
    return new_ads

@app.post("/simulate-optimization")
async def simulate():
    if not db["ads"]:
        return {"error": "No ads generated yet"}
    
    updated_ads = MultiArmedBanditService.simulate_performance(db["ads"])
    db["ads"] = updated_ads
    
    best_ad_id = MultiArmedBanditService.thompson_sampling(updated_ads)
    
    return {
        "ads": updated_ads,
        "winner_id": best_ad_id
    }

@app.get("/ads")
async def get_ads():
    return db["ads"]


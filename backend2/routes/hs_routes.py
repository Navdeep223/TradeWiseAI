from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.hs_classifier import classify_hs_code

router = APIRouter(prefix="/hs", tags=["HS Classification"])

class ClassifyRequest(BaseModel):
    product_description: str

class HSResult(BaseModel):
    rank: int
    hs_code: str
    hs_description: str
    confidence: float
    confidence_pct: str

class ClassifyResponse(BaseModel):
    product_description: str
    results: List[HSResult]

@router.post("/classify", response_model=ClassifyResponse)
def classify(request: ClassifyRequest):
    if not request.product_description.strip():
        raise HTTPException(status_code=400, detail="Product description cannot be empty.")
    try:
        results = classify_hs_code(request.product_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ClassifyResponse(
        product_description=request.product_description,
        results=[HSResult(**r) for r in results],
    )
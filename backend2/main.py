from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from services.origin_optimizer import recommend_origin
from services.hs_classifier import classify_hs_code
from tariff_engine import TariffEngine


app = FastAPI(title="TradeWise AI")

# --------------------------------------------------
# Load Tariff Table (Manual Route Engine)
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GLOBAL_TARIFF_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "global_tariff_table.csv"
)

engine = TariffEngine(GLOBAL_TARIFF_PATH)


# ==================================================
# STEP 1: HS RANKING ENDPOINT
# ==================================================

# ==================================================
# STEP 1: HS RANKING ENDPOINT
# ==================================================

class HSRequest(BaseModel):
    description: str


@app.post("/rank-hs")
def rank_hs(request: HSRequest):

    results = classify_hs_code(request.description)

    if not results:
        raise HTTPException(status_code=400, detail="Unable to classify product")

    ranked = []

    for item in results[:3]:
        ranked.append({
            "rank": item["rank"],
            "hs_code": item["hs_code"],
            "description": item["hs_description"],
            "confidence": item["confidence"],
            "confidence_pct": item["confidence_pct"]
        })

    return {
        "ranked_hs_codes": ranked
    }


# ==================================================
# STEP 2: ANALYSIS USING SELECTED HS
# ==================================================

class AnalyzeRequest(BaseModel):
    selected_hs: str
    destination_country: str
    cost_price: float
    mode: str  # "manual" or "ai"
    origin_country: Optional[str] = None


@app.post("/analyze-selected-hs")
def analyze_selected_hs(request: AnalyzeRequest):

    try:
        hs_code = request.selected_hs.zfill(6)
        destination = request.destination_country.title()
        base_cost = request.cost_price

        if destination.lower() != "india":
            raise HTTPException(
                status_code=400,
                detail="Currently only India as importing country is supported."
            )

        # ======================
        # MANUAL MODE
        # ======================
        if request.mode.lower() == "manual":

            if not request.origin_country:
                raise HTTPException(
                    status_code=400,
                    detail="Origin country required in manual mode."
                )

            origin = request.origin_country.title()

            # Direct route
            direct = engine.calculate_route(
                [origin, destination],
                hs_code
            )

            if direct["total_tariff"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="Tariff data unavailable for selected origin."
                )

            direct["landing_cost"] = round(
                base_cost * (1 + direct["total_tariff"] / 100),
                2
            )

            # Alternate routes
            transit_countries = ["Japan", "Vietnam", "UAE", "Korea"]
            alternates = []

            for country in transit_countries:
                if country in [origin, destination]:
                    continue

                route = [origin, country, destination]
                result = engine.calculate_route(route, hs_code)

                if result["total_tariff"] is None:
                    continue

                result["landing_cost"] = round(
                    base_cost * (1 + result["total_tariff"] / 100),
                    2
                )

                alternates.append(result)

            alternates = sorted(alternates, key=lambda x: x["total_tariff"])[:3]

            return {
                "mode": "manual",
                "selected_hs": hs_code,
                "direct_route": direct,
                "alternate_routes": alternates
            }

        # ======================
        # AI MODE
        # ======================
        elif request.mode.lower() == "ai":

            optimization = recommend_origin(hs_code)

            if "error" in optimization:
                raise HTTPException(status_code=400, detail=optimization["error"])

            min_tariff = optimization["min_tariff"]

            landing_cost = round(
                base_cost * (1 + min_tariff / 100),
                2
            )

            

            return {
                "mode": "ai",
                "selected_hs": hs_code,
                "recommended_origin": optimization["recommended_country"],
                "final_tariff_percent": min_tariff,
                "spread_percent": optimization["spread"],
                "arbitrage_level": optimization["arbitrage_level"],
                "estimated_landing_cost": landing_cost,
                "comparison_table": optimization["comparison"],
                
            }

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid mode. Choose 'manual' or 'ai'."
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
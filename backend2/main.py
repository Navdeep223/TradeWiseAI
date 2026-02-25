from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from services.origin_optimizer import recommend_origin
from services.hs_classifier import classify_hs_code
from services.freight_engine import get_freight_rate
from tariff_engine import TariffEngine


app = FastAPI(title="TradeWise AI")

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# Load Tariff Engine
# ==================================================

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
# STEP 1: HS RANKING
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
            "confidence": item["confidence"]
        })

    return {
        "ranked_hs_codes": ranked
    }


# ==================================================
# STEP 2: ANALYSIS
# ==================================================

class AnalyzeRequest(BaseModel):
    selected_hs: str
    destination_country: str
    cost_price: float
    mode: str
    num_containers: int = 1
    origin_country: Optional[str] = None


@app.post("/analyze-selected-hs")
def analyze_selected_hs(request: AnalyzeRequest):

    hs_code = request.selected_hs.zfill(6)
    destination = request.destination_country.title()
    base_cost = request.cost_price
    num_containers = max(request.num_containers, 1)

    if destination.lower() != "india":
        raise HTTPException(
            status_code=400,
            detail="Currently only India supported as importing country."
        )

    # Total goods value scales with containers
    total_goods_value = base_cost * num_containers

    # ==================================================
    # MANUAL MODE
    # ==================================================

    if request.mode.lower() == "manual":

        if not request.origin_country:
            raise HTTPException(
                status_code=400,
                detail="Origin country required in manual mode."
            )

        origin = request.origin_country.title()

        direct = engine.calculate_route([origin, destination], hs_code)

        base_freight = get_freight_rate(origin, destination) or 0
        freight = base_freight * num_containers

        direct["freight_cost_usd"] = freight
        direct["landing_cost"] = round(
            total_goods_value * (1 + direct["total_tariff"] / 100) + freight,
            2
        )

        transit_countries = ["Japan", "Vietnam", "UAE", "Korea"]
        alternates = []

        for country in transit_countries:
            if country in [origin, destination]:
                continue

            route = [origin, country, destination]
            result = engine.calculate_route(route, hs_code)

            base_freight_alt = get_freight_rate(country, destination) or 0
            freight_alt = base_freight_alt * num_containers

            result["freight_cost_usd"] = freight_alt
            result["landing_cost"] = round(
                total_goods_value * (1 + result["total_tariff"] / 100) + freight_alt,
                2
            )

            alternates.append(result)

        alternates = sorted(alternates, key=lambda x: x["landing_cost"])[:3]

        return {
            "mode": "manual",
            "selected_hs": hs_code,
            "direct_route": direct,
            "alternate_routes": alternates
        }

    # ==================================================
    # AI MODE (FULL LANDED COST BASED)
    # ==================================================

    elif request.mode.lower() == "ai":

        optimization = recommend_origin(hs_code)

        if "error" in optimization:
            raise HTTPException(status_code=400, detail=optimization["error"])

        recommended_origin = optimization["recommended_country"]
        min_tariff = optimization["min_tariff"]

        enriched_comparison = []

        for item in optimization["comparison"]:
            country = item["country"]
            tariff = item["tariff"]

            base_freight = get_freight_rate(country, destination) or 0
            freight = base_freight * num_containers

            landed_cost = round(
                total_goods_value * (1 + tariff / 100) + freight,
                2
            )

            enriched_comparison.append({
                "country": country,
                "tariff_percent": tariff,
                "freight_cost_usd": freight,
                "landed_cost": landed_cost
            })

        recommended_data = next(
            (x for x in enriched_comparison if x["country"] == recommended_origin),
            None
        )

        return {
            "mode": "ai",
            "selected_hs": hs_code,
            "recommended_origin": recommended_origin,
            "final_tariff_percent": min_tariff,
            "spread_percent": optimization["spread"],
            "arbitrage_level": optimization["arbitrage_level"],
            "freight_cost_usd": recommended_data["freight_cost_usd"] if recommended_data else 0,
            "estimated_landing_cost": recommended_data["landed_cost"] if recommended_data else 0,
            "comparison_table": enriched_comparison
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode. Choose 'manual' or 'ai'."
        )
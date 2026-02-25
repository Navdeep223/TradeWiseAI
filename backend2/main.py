from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os

from services.origin_optimizer import recommend_origin
from services.hs_classifier import classify_hs_code
from services.freight_engine import get_freight_rate
from services.llm_service import (
    generate_hs_explanation,
    generate_ai_route_explanation,
    generate_manual_route_explanation
)
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

    # ✅ HS Explanation Added
    hs_explanation = generate_hs_explanation(ranked)

    return {
        "ranked_hs_codes": ranked,
        "hs_explanation": hs_explanation
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
    top_matches: Optional[List[Dict]] = None


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

        second_best = alternates[0] if alternates else None

        explanation_data = {
            "recommended_country": origin,
            "comparison_country": second_best["route"][1] if second_best else "N/A",
            "landed_cost_recommended": direct["landing_cost"],
            "landed_cost_comparison": second_best["landing_cost"] if second_best else 0,
            "cost_difference_percent": round(
                ((second_best["landing_cost"] - direct["landing_cost"]) /
                 second_best["landing_cost"]) * 100,
                2
            ) if second_best else 0,
            "tariff_rate_recommended": direct["total_tariff"],
            "tariff_rate_comparison": second_best["total_tariff"] if second_best else 0,
            "freight_cost_recommended": direct["freight_cost_usd"],
            "freight_cost_comparison": second_best["freight_cost_usd"] if second_best else 0,
            "risk_score": 0,
            "main_risk_driver": "Tariff variation",
            "most_sensitive_variable": "Freight rate",
            "mode": "Manual"
        }

        explanation = generate_manual_route_explanation(explanation_data)

        return {
            "mode": "manual",
            "selected_hs": hs_code,
            "direct_route": direct,
            "alternate_routes": alternates,
            "explanation": explanation
        }

    # ==================================================
    # AI MODE
    # ==================================================

    elif request.mode.lower() == "ai":

        optimization = recommend_origin(hs_code)

        if "error" in optimization:
            raise HTTPException(status_code=400, detail=optimization["error"])

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

        sorted_comparison = sorted(enriched_comparison, key=lambda x: x["landed_cost"])

        best = sorted_comparison[0]
        second = sorted_comparison[1] if len(sorted_comparison) > 1 else None

        cost_diff_percent = round(
            ((second["landed_cost"] - best["landed_cost"]) /
             second["landed_cost"]) * 100,
            2
        ) if second else 0

        explanation_data = {
            "recommended_country": best["country"],
            "comparison_country": second["country"] if second else "N/A",
            "landed_cost_recommended": best["landed_cost"],
            "landed_cost_comparison": second["landed_cost"] if second else 0,
            "cost_difference_percent": cost_diff_percent,
            "tariff_rate_recommended": best["tariff_percent"],
            "tariff_rate_comparison": second["tariff_percent"] if second else 0,
            "freight_cost_recommended": best["freight_cost_usd"],
            "freight_cost_comparison": second["freight_cost_usd"] if second else 0,
            "risk_score": 0,
            "main_risk_driver": "Tariff differential",
            "most_sensitive_variable": "Freight rate",
            "mode": "AI"
        }

        explanation = generate_ai_route_explanation(explanation_data)

        return {
            "mode": "ai",
            "selected_hs": hs_code,
            "recommended_origin": best["country"],
            "freight_cost_usd": best["freight_cost_usd"],
            "estimated_landing_cost": best["landed_cost"],
            "comparison_table": enriched_comparison,
            "explanation": explanation
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode. Choose 'manual' or 'ai'."
        )
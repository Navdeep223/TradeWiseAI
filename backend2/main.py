from fastapi import FastAPI
from pydantic import BaseModel
import os

from services.hs_classifier import classify_hs_code
from tariff_engine import TariffEngine

app = FastAPI(title="TradeWise AI")


# ---- Load Global Tariff Table ----

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GLOBAL_TARIFF_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "global_tariff_table.csv"
)

engine = TariffEngine(GLOBAL_TARIFF_PATH)


# ---- Request Model ----

class ProductRequest(BaseModel):
    description: str
    origin_country: str


# ---- Endpoint ----

@app.post("/analyze-product")
def analyze_product(request: ProductRequest):

    classification_results = classify_hs_code(request.description)
    top_hs6 = classification_results[0]["hs_code"]

    origin = request.origin_country.strip()

    valid_routes = []
    direct_result = None

    # ---- DIRECT ROUTE ----
    try:
        direct_result = engine.calculate_route(
            [origin, "India"],
            top_hs6
        )
        valid_routes.append({
            "type": "direct",
            **direct_result
        })
    except:
        pass


    # ---- FIND TRANSIT OPTIONS ----
    possible_transits = engine.df[
        engine.df["exporter"] == origin
    ]["importer"].unique()

    possible_transits = [
        country for country in possible_transits
        if country not in ["India", origin]
    ]

    for transit in possible_transits:
        try:
            result = engine.calculate_route(
                [origin, transit, "India"],
                top_hs6
            )
            valid_routes.append({
                "type": "alternate",
                **result
            })
        except:
            continue


    valid_routes = [
        r for r in valid_routes
        if isinstance(r.get("total_tariff"), (int, float))
    ]

    if not valid_routes:
        return {
            "classification": classification_results,
            "message": "No valid tariff routes found."
        }

    # ---- FIND BEST ROUTE ----
    best_route = min(valid_routes, key=lambda x: x["total_tariff"])

    savings_info = None

    if direct_result and best_route:

        direct_tariff = direct_result["total_tariff"]
        best_tariff = best_route["total_tariff"]

        difference = round(direct_tariff - best_tariff, 4)

        if difference > 0:
            percentage_saving = round((difference / direct_tariff) * 100, 2) if direct_tariff != 0 else 0

            savings_info = {
                "direct_tariff": direct_tariff,
                "best_route_tariff": best_tariff,
                "absolute_saving": difference,
                "percentage_saving": percentage_saving
            }

    recommendation = None

    if best_route["type"] == "direct":
        recommendation = "Direct import is the most cost-efficient option."
    else:
        recommendation = "Alternate route is cheaper than direct import."

    return {
        "classification": classification_results,
        "direct_route": direct_result,
        "best_route": best_route,
        "all_valid_routes": valid_routes,
        "savings_analysis": savings_info,
        "recommendation": recommendation
    }
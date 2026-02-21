from tariff_engine import get_india_tariff
from route_engine import get_china_to_country_tariff

INTERMEDIATE_COUNTRIES = ["Japan", "Korea", "UAE", "Vietnam"]


def optimize_route(origin_country, hs6):
    origin_country = origin_country.strip().lower()
    hs6 = str(hs6).strip().zfill(6)

    if origin_country != "china":
        return {"error": "Currently only China supported as origin."}

    # ----------------------------------
    # Direct route
    # ----------------------------------
    direct_tariff = get_india_tariff("china", hs6)

    if direct_tariff is None:
        return {"error": "HS code not found in India tariff dataset."}

    best_route = {
        "route": "China → India",
        "total_tariff": round(direct_tariff, 4)
    }

    # ----------------------------------
    # Intermediate routes
    # ----------------------------------
    for country in INTERMEDIATE_COUNTRIES:

        china_to_x = get_china_to_country_tariff(country, hs6)
        x_to_india = get_india_tariff(country, hs6)

        if china_to_x is None or x_to_india is None:
            continue

        total = china_to_x + x_to_india

        if total < best_route["total_tariff"]:
            best_route = {
                "route": f"China → {country} → India",
                "total_tariff": round(total, 4)
            }

    return {
        "hs6": hs6,
        "direct_tariff": round(direct_tariff, 4),
        "best_route": best_route
    }
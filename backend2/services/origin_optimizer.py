import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Load dataset once (on module load)
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "india_import_tariffs_long.csv"

df = pd.read_csv(DATA_PATH)

# Ensure HS6 is always string with leading zeros
df["hs6"] = df["hs6"].astype(str).str.zfill(6)


# --------------------------------------------------
# Core Optimization Function
# --------------------------------------------------

def recommend_origin(hs_code: str):

    hs_code = str(hs_code).zfill(6)

    # Filter for this HS code where importer = India
    filtered = df[
        (df["hs6"] == hs_code) &
        (df["importer"].str.lower() == "india")
    ]

    if filtered.empty:
        return {"error": "HS code not found in tariff dataset."}

    # Build exporter -> tariff dictionary
    tariffs = {}

    for _, row in filtered.iterrows():
        exporter = row["exporter"]
        tariff = row["tariff"]

        if pd.notnull(tariff):
            tariffs[exporter] = float(tariff)

    if not tariffs:
        return {"error": "No tariff data available for this HS code."}

    # Sort by tariff (ascending)
    sorted_tariffs = sorted(tariffs.items(), key=lambda x: x[1])

    min_country, min_tariff = sorted_tariffs[0]
    max_tariff = sorted_tariffs[-1][1]

    spread = max_tariff - min_tariff
    avg_tariff = sum(tariffs.values()) / len(tariffs)
    savings_vs_avg = avg_tariff - min_tariff

    # Arbitrage classification
    if spread >= 15:
        arbitrage_level = "High"
    elif spread >= 5:
        arbitrage_level = "Moderate"
    else:
        arbitrage_level = "Low"

    return {
        "hs6": hs_code,
        "recommended_country": min_country,
        "min_tariff": round(min_tariff, 2),
        "spread": round(spread, 2),
        "average_tariff": round(avg_tariff, 2),
        "savings_vs_average": round(savings_vs_avg, 2),
        "arbitrage_level": arbitrage_level,
        "comparison": [
            {
                "country": country,
                "tariff": round(tariff, 2)
            }
            for country, tariff in sorted_tariffs
        ]
    }
import os
import pandas as pd

# -------------------------------------------------
# Resolve project root correctly (MAKEATHON level)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

csv_path = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "sea_freight_40ft_ocean.csv"
)

_freight_df = pd.read_csv(csv_path)

freight_lookup = {
    (row["origin_country"], row["destination_country"]): row["rate_usd"]
    for _, row in _freight_df.iterrows()
}


def get_freight_rate(origin_country: str, destination_country: str = "India"):
    return freight_lookup.get((origin_country, destination_country))
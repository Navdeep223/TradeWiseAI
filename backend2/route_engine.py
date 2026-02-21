import os
import pandas as pd

# -------------------------------------------------
# Resolve project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

csv_path = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "china_routes.csv"
)

# -------------------------------------------------
# Load dataset
# -------------------------------------------------
routes_df = pd.read_csv(csv_path)

# Normalize columns
routes_df.columns = routes_df.columns.str.strip().str.lower()

# Normalize country columns
routes_df["reporting_country"] = routes_df["reporting_country"].astype(str).str.strip().str.lower()
routes_df["partner_country"] = routes_df["partner_country"].astype(str).str.strip().str.lower()

# Normalize HS codes
routes_df["hs_code_6digit"] = (
    routes_df["hs_code_6digit"]
    .astype(str)
    .str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .str.zfill(6)
)

# Filter only China exports (China → X)
routes_df = routes_df[routes_df["partner_country"] == "china"]

# Optional: filter single year (recommended)
routes_df = routes_df[routes_df["year"] == 2023]

route_lookup = {}

for _, row in routes_df.iterrows():
    importer = row["reporting_country"]      # Japan, Korea, UAE, etc.
    hs6 = row["hs_code_6digit"]
    tariff = float(row["tariff_rate"])

    route_lookup[(importer, hs6)] = tariff


def get_china_to_country_tariff(country, hs6):
    country = country.strip().lower()
    hs6 = str(hs6).strip().replace(".0", "").zfill(6)

    return route_lookup.get((country, hs6), None)
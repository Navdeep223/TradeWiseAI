import os
import pandas as pd

# Get absolute path to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build path to CSV
file_path = os.path.join(BASE_DIR, "data", "processed", "master_tariff_matrix.csv")

# Load CSV
df = pd.read_csv(file_path)

# Normalize column names (safe)
df.columns = df.columns.str.strip().str.lower()

# Ensure hs6 column exists
if "hs6" not in df.columns:
    raise Exception(f"Expected column 'hs6' not found. Columns available: {df.columns.tolist()}")

# Ensure hs6 is string
df["hs6"] = df["hs6"].astype(str)

# Convert dataframe to dictionary for fast lookup
tariff_dict = df.set_index("hs6").to_dict(orient="index")


def get_tariff_data(hs_code: str):
    return tariff_dict.get(str(hs_code))
# final_clean_master.py
# Run with: python "C:\Users\prana\makethon\dataset\final_clean_master.py"

import pandas as pd
from pathlib import Path
import re

print("===== THIS IS THE CORRECT FILE BEING RUN =====")
print("File path:", __file__)
print("Current working directory:", Path.cwd())

# ────────────────────────────────────────────────
# This path is taken directly from your File Explorer screenshot
# ────────────────────────────────────────────────
BASE_FOLDER = Path(r"C:\Users\prana\makethon\dataset")
OUTPUT_FOLDER = BASE_FOLDER / "cleaned"

print("\nChecking base folder:")
print("Path:", BASE_FOLDER)
print("Exists?", BASE_FOLDER.exists())
print("Is directory?", BASE_FOLDER.is_dir())

if not BASE_FOLDER.exists():
    print("FOLDER NOT FOUND - stopping here")
    print("Double-check the spelling: makethon (not makathon, makeathon, etc.)")
    exit(1)

# Your files — exact names from your screenshot
ORIGIN_MAP = {
    "india_china_2023.csv":   "China",
    "india_japan_2023.csv":   "Japan",
    "india_korea_2023.csv":   "South Korea",
    "india_uae_2023.csv":     "UAE",
    "india_vietnam_2023.csv": "Vietnam",
}

print("\nFile check:")
for fn in ORIGIN_MAP:
    exists = (BASE_FOLDER / fn).exists()
    print(f"  {fn:25} → {'EXISTS' if exists else 'MISSING'}")

if all(not (BASE_FOLDER / fn).exists() for fn in ORIGIN_MAP):
    print("\nAll files missing → nothing to process")
    print("Check file names exactly match (including year and .csv)")
    exit(1)

# ────────────────────────────────────────────────
# Cleaning functions
# ────────────────────────────────────────────────
def clean_hs(x):
    if pd.isna(x): return None
    s = re.sub(r'[^0-9]', '', str(x).strip())
    if len(s) < 4: return None
    return s.zfill(8)[:8]

def clean_rate(x):
    if pd.isna(x): return 0.0
    try:
        return float(re.sub(r'[^0-9.]', '', str(x).strip()))
    except:
        return 0.0

# ────────────────────────────────────────────────
# Main processing
# ────────────────────────────────────────────────
all_6dig = []

for filename, origin in ORIGIN_MAP.items():
    path = BASE_FOLDER / filename
    if not path.exists():
        continue

    print(f"\nReading: {filename}")

    df = pd.read_csv(path, dtype=str)

    df.columns = df.columns.str.strip().str.lower()

    rename = {
        "productcode": "hs",
        "advalorem": "advalorem",
        "measuren nonadvalaffected": "treatment",
        "measurennonadvalaffected": "treatment",
        "partnername": "partner",
        "year": "year",
    }
    df.rename(columns=rename, inplace=True)

    if "hs" not in df.columns:
        print("  No 'hs' or 'productcode' column → skip")
        continue

    df["HS8"] = df["hs"].apply(clean_hs)
    df = df[df["HS8"].notna()].copy()

    df["AdValorem"] = df.get("advalorem", 0.0).apply(clean_rate)
    df["Origin"] = origin

    keep = ["Origin", "HS8", "AdValorem", "treatment", "partner", "year"]
    df = df[[c for c in keep if c in df.columns]]

    # Save 8-digit
    out8 = OUTPUT_FOLDER / f"clean_8dig_{origin.lower().replace(' ','_')}_2023.xlsx"
    df.to_excel(out8, index=False)
    print(f"  → 8-digit saved: {out8.name} ({len(df)} rows)")

    # 6-digit agg
    df["HS6"] = df["HS8"].str[:6]
    agg = df.groupby(["Origin", "HS6"]).agg({
        "AdValorem": "min",
        "treatment": "first",
        "partner": "first",
        "year": "first",
    }).reset_index()

    out6 = OUTPUT_FOLDER / f"agg_6dig_{origin.lower().replace(' ','_')}_2023.xlsx"
    agg.to_excel(out6, index=False)
    print(f"  → 6-digit saved: {out6.name} ({len(agg)} rows)")

    all_6dig.append(agg)

# Combined
if all_6dig:
    combined = pd.concat(all_6dig, ignore_index=True).sort_values(["Origin", "HS6"])
    final_path = OUTPUT_FOLDER / "all_countries_6dig_2023.xlsx"
    combined.to_excel(final_path, index=False)
    print("\n" + "="*70)
    print("FINISHED")
    print("Combined file created:", final_path.name)
    print("Total rows:", len(combined))
    print("Unique HS6:", combined["HS6"].nunique())
    print("="*70)
else:
    print("No files were processed successfully")
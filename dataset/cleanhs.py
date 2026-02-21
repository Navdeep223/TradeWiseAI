import pandas as pd

# Load HS classification file
df = pd.read_excel("HSProducts.xls")

# Keep only Tier 3 (6-digit level)
df = df[df["Tier"] == 3].copy()

# Ensure ProductCode is string and 6-digit
df["ProductCode"] = df["ProductCode"].astype(str).str.zfill(6)

# Rename columns
df = df[["ProductCode", "Product Description"]]
df.rename(columns={
    "ProductCode": "HS6",
    "Product Description": "HS_Description"
}, inplace=True)

# Save clean HS6 classification file
df.to_csv("hs6_classification_clean.csv", index=False)

print("HS6 classification dataset created.")
print("Total HS6 codes:", len(df))
print(df.head())
import pandas as pd

df = pd.read_csv("master_tariff_2023.csv", dtype={"HS6": str})

print("Total rows:", len(df))

print("\nUnique partners:")
print(df["PartnerName"].value_counts())

print("\nUnique HS6 codes per partner:")
print(df.groupby("PartnerName")["HS6"].nunique())

duplicates = df.duplicated(subset=["PartnerName", "HS6"]).sum()
print("\nDuplicate rows:", duplicates)

print("\nHS6 length check:")
print(df["HS6"].astype(str).str.len().value_counts())

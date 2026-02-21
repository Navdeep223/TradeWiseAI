import os
import pandas as pd

DATASET_FOLDER = "."
YEAR = "2023"


def load_file(filepath):
    for enc in ["utf-8", "utf-8-sig", "cp1252", "latin1"]:
        try:
            return pd.read_csv(filepath, encoding=enc, dtype=str)
        except:
            continue
    raise Exception(f"Could not read file: {filepath}")


def clean_tariff_file(filepath):
    print(f"\nProcessing {filepath}...")

    df = load_file(filepath)

    # Keep only needed columns
    df = df[["ProductCode", "PartnerName", "Year", "AdValorem"]]

    # Force ProductCode to string
    df["ProductCode"] = df["ProductCode"].astype(str)

    # Remove decimal artifacts
    df["ProductCode"] = df["ProductCode"].str.split(".").str[0]

    # Pad to 8 digits
    df["ProductCode"] = df["ProductCode"].str.zfill(8)

    # Convert to HS6
    df["HS6"] = df["ProductCode"].str[:6]

    # Keep only numeric 6-digit codes
    df = df[df["HS6"].str.isnumeric()]
    df = df[df["HS6"].str.len() == 6]

    # Convert tariff to numeric
    df["Tariff"] = pd.to_numeric(df["AdValorem"], errors="coerce")
    df = df.dropna(subset=["Tariff"])

    # -------------------------
    # FIX PARTNER LABELING
    # -------------------------

    unique_partners = df["PartnerName"].astype(str).unique()

    # China (MFN shown as World)
    if "World" in unique_partners:
        df["PartnerName"] = "China"
        df["Agreement"] = "MFN"

    # Vietnam (ASEAN FTA case)
    elif "ASEAN" in unique_partners:
        df["PartnerName"] = "Vietnam"
        df["Agreement"] = "ASEAN-India FTA"

    # Others (Japan, Korea, UAE)
    else:
        df["Agreement"] = "Bilateral/FTA"

    # Final structure
    df = df[["PartnerName", "Agreement", "HS6", "Tariff"]]

    # Remove duplicates inside file
    df = df.drop_duplicates(subset=["PartnerName", "HS6"])

    print("Rows after cleaning:", len(df))

    return df


def main():
    all_data = []

    for file in os.listdir(DATASET_FOLDER):
        if file.startswith("india_") and file.endswith(".csv"):
            df_clean = clean_tariff_file(file)
            all_data.append(df_clean)

    master_df = pd.concat(all_data, ignore_index=True)

    # Final dedupe across all files
    master_df = master_df.drop_duplicates(subset=["PartnerName", "HS6"])

    # Final HS6 safety check
    master_df = master_df[master_df["HS6"].str.len() == 6]

    master_df.to_csv("master_tariff_2023_final.csv", index=False)

    print("\nMaster dataset created: master_tariff_2023_final.csv")
    print("Total rows:", len(master_df))

    print("\nHS6 length check:")
    print(master_df["HS6"].str.len().value_counts())

    print("\nPartner distribution:")
    print(master_df["PartnerName"].value_counts())


if __name__ == "__main__":
    main()
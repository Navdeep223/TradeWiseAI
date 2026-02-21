import pandas as pd
import os


def preprocess_file(filepath):
    print(f"\nProcessing: {os.path.basename(filepath)}")

    # ---- SAFE CSV LOADING (handles Excel encoding issues) ----
    try:
        df = pd.read_csv(filepath, dtype=str, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, dtype=str, encoding="latin1")

    df.columns = df.columns.str.strip()

    # ---- EXTRACT COUNTRY FROM FILENAME ----
    filename = os.path.basename(filepath)
    country_name = (
        filename.replace(".csv", "")
        .replace("india_", "")
        .replace("_2023", "")
        .replace("_", " ")
        .title()
    )

    df["Country"] = country_name

    # ---- CLEAN PRODUCT CODE ----
    df["ProductCode"] = (
        df["ProductCode"]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
    )

    # Remove null / blank codes
    df = df[df["ProductCode"].notna()]
    df = df[df["ProductCode"] != ""]

    # Ensure 8-digit format (restore lost leading zeros)
    df["ProductCode"] = df["ProductCode"].str.zfill(8)

    # Convert HS8 → HS6
    df["HS6"] = df["ProductCode"].str[:6]

    # ---- CLEAN TARIFF COLUMN ----
    df["AdValorem"] = (
        df["AdValorem"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    df["AdValorem"] = pd.to_numeric(df["AdValorem"], errors="coerce")

    # Remove rows where tariff missing
    df = df[df["AdValorem"].notna()]

    # Remove duplicates
    df = df.drop_duplicates()

    # ---- AGGREGATE TO HS6 LEVEL ----
    df_hs6 = (
        df.groupby(["HS6", "Country"], as_index=False)
        .agg({"AdValorem": "mean"})
    )

    df_hs6["AdValorem"] = df_hs6["AdValorem"].round(2)

    # ---- SAVE CLEAN FILE ----
    clean_filename = filepath.replace(".csv", "_clean_hs6.csv")
    df_hs6.to_csv(clean_filename, index=False)

    print(f"Saved → {os.path.basename(clean_filename)}")
    print(f"Final HS6 rows: {len(df_hs6)}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(current_dir):
        if file.endswith(".csv") and "clean" not in file:
            full_path = os.path.join(current_dir, file)
            preprocess_file(full_path)


if __name__ == "__main__":
    main()
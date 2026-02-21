import pandas as pd
import os


def normalize_india_matrix(input_path, output_path):
    """
    Converts matrix-style India import tariff file into long format.

    Input format:
    HS6 | China | Japan | Korea | UAE | Vietnam

    Output format:
    exporter | importer | hs6 | tariff
    """

    df = pd.read_csv(input_path)

    # Clean HS6
    df["HS6"] = df["HS6"].astype(str).str.zfill(6)

    # Convert matrix to long format
    long_df = df.melt(
        id_vars=["HS6"],
        var_name="exporter",
        value_name="tariff"
    )

    long_df = long_df.rename(columns={"HS6": "hs6"})

    # This matrix represents India importing
    long_df["importer"] = "India"

    # Clean country names
    long_df["exporter"] = long_df["exporter"].astype(str).str.strip()
    long_df["importer"] = long_df["importer"].astype(str).str.strip()

    # Ensure numeric tariffs
    long_df["tariff"] = pd.to_numeric(long_df["tariff"], errors="raise")

    # Reorder columns
    long_df = long_df[["exporter", "importer", "hs6", "tariff"]]

    long_df.to_csv(output_path, index=False)

    print("✅ Normalized file saved at:")
    print(output_path)


if __name__ == "__main__":
    # Get project root (MAKEATHON folder)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "master_tariff_matrix.csv"
    )

    output_file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "india_import_tariffs_long.csv"
    )

    print("Reading from:", input_file)
    print("Saving to:", output_file)

    normalize_india_matrix(input_file, output_file)
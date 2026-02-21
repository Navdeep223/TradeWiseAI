import pandas as pd
import os


def normalize_route_file(filepath):
    """
    Converts route-style files into:
    exporter | importer | hs6 | tariff
    """

    df = pd.read_csv(filepath)

    df.columns = df.columns.str.lower().str.strip()

    required_cols = {"reporting_country", "partner_country", "hs_code_6digit", "tariff_rate"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"File {filepath} missing required columns")

    normalized = pd.DataFrame({
        "exporter": df["partner_country"].astype(str).str.strip(),
        "importer": df["reporting_country"].astype(str).str.strip(),
        "hs6": df["hs_code_6digit"].astype(str).str.zfill(6),
        "tariff": pd.to_numeric(df["tariff_rate"], errors="raise")
    })

    return normalized


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

    # ---- Load India long matrix ----
    india_file = os.path.join(DATA_DIR, "india_import_tariffs_long.csv")
    india_df = pd.read_csv(india_file)

    india_df.columns = india_df.columns.str.lower().str.strip()
    india_df["hs6"] = india_df["hs6"].astype(str).str.zfill(6)
    india_df["tariff"] = pd.to_numeric(india_df["tariff"], errors="raise")

    all_dfs = [india_df]

    # ---- Add other route files here ----
    route_files = [
        "china_routes.csv",
        # add more files here later if needed
    ]

    for file in route_files:
        filepath = os.path.join(DATA_DIR, file)
        print(f"Processing: {filepath}")
        normalized_df = normalize_route_file(filepath)
        all_dfs.append(normalized_df)

    # ---- Combine everything ----
    global_df = pd.concat(all_dfs, ignore_index=True)

    # Remove exact duplicates (safety)
    global_df = global_df.drop_duplicates()

    # Final sanity checks
    global_df["hs6"] = global_df["hs6"].astype(str).str.zfill(6)
    global_df["tariff"] = pd.to_numeric(global_df["tariff"], errors="raise")

    # Save final table
    output_path = os.path.join(DATA_DIR, "global_tariff_table.csv")
    global_df.to_csv(output_path, index=False)

    print("✅ Global tariff table created at:")
    print(output_path)
    print("Total rows:", len(global_df))
import pandas as pd
import os

def main():
    folder = os.path.dirname(os.path.abspath(__file__))

    all_data = []

    for file in os.listdir(folder):
        if file.endswith("_clean_hs6.csv"):
            df = pd.read_csv(os.path.join(folder, file))
            all_data.append(df)

    # Combine all countries
    master = pd.concat(all_data, ignore_index=True)

    # Pivot into matrix
    matrix = master.pivot(index="HS6", columns="Country", values="AdValorem")

    # Fill missing tariffs with 0 (or keep NaN if you want)
    matrix = matrix.fillna(0)

    matrix = matrix.reset_index()

    matrix.to_csv("master_tariff_matrix.csv", index=False)

    print("Master tariff matrix created.")
    print("Total HS6 rows:", len(matrix))


if __name__ == "__main__":
    main()
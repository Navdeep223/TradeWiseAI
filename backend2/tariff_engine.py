import pandas as pd


class TariffEngine:

    def __init__(self, csv_path: str):
        print(f"[TariffEngine] Loading tariff table from: {csv_path}")

        self.df = pd.read_csv(
            csv_path,
            dtype={"hs6": str}
        )

        # ---- NORMALIZATION ----
        self.df["hs6"] = self.df["hs6"].astype(str).str.strip().str.zfill(6)
        self.df["exporter"] = self.df["exporter"].astype(str).str.strip().str.lower()
        self.df["importer"] = self.df["importer"].astype(str).str.strip().str.lower()
        self.df["tariff"] = pd.to_numeric(self.df["tariff"], errors="coerce")

        print(f"[TariffEngine] Loaded {len(self.df)} rows.")

    # -----------------------------------------------------

    def get_tariff(self, exporter: str, importer: str, hs6: str):

        exporter = exporter.strip().lower()
        importer = importer.strip().lower()
        hs6 = str(hs6).strip().zfill(6)

        match = self.df[
            (self.df["exporter"] == exporter) &
            (self.df["importer"] == importer) &
            (self.df["hs6"] == hs6)
        ]

        if match.empty:
            raise ValueError(
                f"No tariff found for {exporter} → {importer} (HS6: {hs6})"
            )

        return float(match.iloc[0]["tariff"])

    # -----------------------------------------------------

    def calculate_route(self, route: list, hs6: str):

        breakdown = []
        total = 0

        for i in range(len(route) - 1):

            exporter = route[i]
            importer = route[i + 1]

            tariff = self.get_tariff(exporter, importer, hs6)

            breakdown.append({
                "from": exporter.title(),
                "to": importer.title(),
                "tariff": tariff
            })

            total += tariff

        return {
            "hs6": str(hs6).zfill(6),
            "route": " → ".join([r.title() for r in route]),
            "breakdown": breakdown,
            "total_tariff": round(total, 4)
        }
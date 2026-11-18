
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SIM_PATH = ROOT / "calibration" / "results" / "processed" / "alpha_sensor_counts.csv"
REFERENCE_PATH = ROOT / "calibration" / "results" / "processed" / "calibration_hourly_reference.csv"
OUTPUT_DIR = ROOT / "calibration" / "results" / "processed"

REFERENCE_YEAR = 2025
REFERENCE_MONTH = 10
REFERENCE_DAY_TYPE = "weekday"
REFERENCE_HOUR = 8


def main():
    simulated = pd.read_csv(SIM_PATH)
    reference = pd.read_csv(REFERENCE_PATH)

    reference = reference[
        (reference["year"] == REFERENCE_YEAR)
        & (reference["month"] == REFERENCE_MONTH)
        & (reference["day_type"] == REFERENCE_DAY_TYPE)
        & (reference["hour"] == REFERENCE_HOUR)
    ].copy()

    reference = reference.rename(columns={
        "avg": "observed_avg",
        "median": "observed_median",
        "min": "observed_min",
        "max": "observed_max"
    })

    comparison = simulated.merge(
        reference[
            ["sensor", "observed_avg", "observed_median",
             "observed_min", "observed_max"]
        ],
        left_on="sensor_name",
        right_on="sensor",
        how="left"
    )

    if comparison["observed_avg"].isna().any():
        raise ValueError("Brak danych referencyjnych dla któregoś licznika.")

    comparison["absolute_error"] = (
        comparison["simulated_passages"] - comparison["observed_avg"]
    ).abs()

    comparison["relative_error_pct"] = (
        comparison["absolute_error"] / comparison["observed_avg"] * 100
    )

    metrics = []

    for strategy, group in comparison.groupby("strategy"):
        errors = group["simulated_passages"] - group["observed_avg"]

        metrics.append({
            "strategy": strategy,
            "MAE": np.mean(np.abs(errors)),
            "RMSE": np.sqrt(np.mean(errors ** 2)),
            "WAPE_pct": (
                np.abs(errors).sum()
                / group["observed_avg"].sum() * 100
            )
        })

    metrics_df = pd.DataFrame(metrics)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    comparison.to_csv(
        OUTPUT_DIR / "alpha_vs_reference.csv",
        index=False
    )

    metrics_df.to_csv(
        OUTPUT_DIR / "alpha_calibration_metrics.csv",
        index=False
    )

    print("\nPORÓWNANIE Z RZECZYWISTOŚCIĄ:")
    print(comparison[
        ["sensor_name", "strategy", "observed_avg",
         "simulated_passages", "absolute_error",
         "relative_error_pct"]
    ].to_string(index=False))

    print("\nMETRYKI:")
    print(metrics_df.to_string(index=False))

    print(f"\nWyniki zapisano w: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

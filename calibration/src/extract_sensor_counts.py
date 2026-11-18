
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

CANDIDATES_PATH = ROOT / "calibration" / "results" / "processed" / "sensor_edge_candidates_alpha.csv"
RESULTS_DIR = ROOT / "results"
OUTPUT_DIR = ROOT / "calibration" / "results" / "processed"

STRATEGIES = {
    "shortest": RESULTS_DIR / "alpha_shortest.csv",
    "bike_preferred": RESULTS_DIR / "alpha_bike_preferred.csv",
}


def main():
    candidates = pd.read_csv(
        CANDIDATES_PATH,
        dtype={"u": str, "v": str, "key": str}
    )

    candidates = candidates[
        candidates["coord_source"] == "metadane_licznikow.csv"
    ].copy()

    if candidates.empty:
        raise ValueError("Brak potwierdzonych roboczo kandydatów liczników.")

    summaries = []
    details = []

    for strategy, path in STRATEGIES.items():
        if not path.exists():
            raise FileNotFoundError(f"Brak wyników symulacji: {path}")

        simulated = pd.read_csv(
            path,
            dtype={"u": str, "v": str, "key": str}
        )

        matched = candidates.merge(
            simulated,
            on=["u", "v", "key"],
            how="left"
        )

        matched["simulated_passages"] = (
            matched["simulated_passages"].fillna(0).astype(int)
        )

        matched["strategy"] = strategy
        details.append(matched)

        summary = (
            matched.groupby("sensor_name")
            .agg(
                candidate_edges=("u", "count"),
                edges_with_traffic=("simulated_passages", lambda x: (x > 0).sum()),
                simulated_passages=("simulated_passages", "sum")
            )
            .reset_index()
        )

        summary["strategy"] = strategy
        summaries.append(summary)

    summary_df = pd.concat(summaries, ignore_index=True)
    details_df = pd.concat(details, ignore_index=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(
        OUTPUT_DIR / "alpha_sensor_counts.csv",
        index=False
    )

    details_df.to_csv(
        OUTPUT_DIR / "alpha_sensor_edge_counts.csv",
        index=False
    )

    print("\nPRZEJAZDY PRZEZ LICZNIKI:")
    print(summary_df.to_string(index=False))

    print("\nSZCZEGÓŁY KRAWĘDZI:")
    print(
        details_df[
            ["sensor_name", "strategy", "u", "v", "simulated_passages"]
        ].to_string(index=False)
    )

    print(f"\nWyniki zapisano w: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

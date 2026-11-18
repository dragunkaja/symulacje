
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import model_alpha as model

CANDIDATES_PATH = ROOT / "calibration/results/processed/sensor_edge_candidates_alpha.csv"
REFERENCE_PATH = ROOT / "calibration/results/processed/calibration_hourly_reference.csv"
OUTPUT_DIR = ROOT / "calibration/results/processed"

N_VALUES = [400, 500, 600, 700, 717, 800, 900, 1000, 1100]
BIKE_FACTORS = [1.00, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70]

SENSORS = ["Kotlarska", "Grzegórzecka"]


def load_data():
    candidates = pd.read_csv(
        CANDIDATES_PATH,
        dtype={"u": str, "v": str, "key": str}
    )

    candidates = candidates[
        candidates["coord_source"] == "metadane_licznikow.csv"
    ]

    reference = pd.read_csv(REFERENCE_PATH)

    reference = reference[
        (reference["year"] == 2025)
        & (reference["month"] == 10)
        & (reference["day_type"] == "weekday")
        & (reference["hour"] == 8)
    ]

    targets = reference.set_index("sensor")["avg"].to_dict()

    if any(sensor not in targets for sensor in SENSORS):
        raise ValueError("Brak danych referencyjnych.")

    return candidates, targets



def count_sensor_passages(crossings, candidates):
    normalized_crossings = {
        (str(u), str(v), str(key)): count
        for (u, v, key), count in crossings.items()
    }

    result = {sensor: 0 for sensor in SENSORS}
    matched_edges = 0

    for row in candidates.itertuples(index=False):
        edge = (str(row.u), str(row.v), str(row.key))

        if edge in normalized_crossings:
            matched_edges += 1

        result[row.sensor_name] += normalized_crossings.get(edge, 0)

    if matched_edges == 0:
        raise RuntimeError(
            "Nie znaleziono żadnej krawędzi licznika w wynikach symulacji."
        )

    return result


def calculate_metrics(counts, targets):
    errors = np.array([
        counts[sensor] - targets[sensor]
        for sensor in SENSORS
    ])

    return {
        "MAE": np.mean(np.abs(errors)),
        "RMSE": np.sqrt(np.mean(errors ** 2)),
        "WAPE_pct": (
            np.abs(errors).sum()
            / sum(targets.values()) * 100
        )
    }


def main():
    candidates, targets = load_data()
    graph = model.load_network(model.GRAPH_PATH)

    demand_results = []

    print("KALIBRACJA LICZBY AGENTÓW")

    for n in N_VALUES:
        trips = model.draw_trips(
            graph,
            n,
            seed=model.SEED
        )

        crossings, _ = model.simulate(
            graph,
            trips,
            "shortest"
        )

        counts = count_sensor_passages(crossings, candidates)
        metrics = calculate_metrics(counts, targets)

        demand_results.append({
            "agents": n,
            **counts,
            **metrics
        })

        print(
            f"N={n}: "
            f"Kotlarska={counts['Kotlarska']}, "
            f"Grzegorzecka={counts['Grzegórzecka']}, "
            f"MAE={metrics['MAE']:.2f}"
        )

    demand_df = pd.DataFrame(demand_results)
    best_row = demand_df.sort_values(
        ["MAE", "RMSE"]
    ).iloc[0]

    best_n = int(best_row["agents"])

    trips = model.draw_trips(
        graph,
        best_n,
        seed=model.SEED
    )

    factor_results = []

    print("\nKALIBRACJA PREFERENCJI INFRASTRUKTURY")

    for factor in BIKE_FACTORS:
        model.BIKE_PREFERENCE_FACTOR = factor

        crossings, _ = model.simulate(
            graph,
            trips,
            "bike_preferred"
        )

        counts = count_sensor_passages(crossings, candidates)
        metrics = calculate_metrics(counts, targets)

        factor_results.append({
            "agents": best_n,
            "bike_preference_factor": factor,
            **counts,
            **metrics
        })

        print(
            f"beta={factor}: "
            f"Kotlarska={counts['Kotlarska']}, "
            f"Grzegorzecka={counts['Grzegórzecka']}, "
            f"MAE={metrics['MAE']:.2f}"
        )

    factor_df = pd.DataFrame(factor_results)

    best_factor = factor_df.sort_values(
        ["MAE", "RMSE"]
    ).iloc[0]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    demand_df.to_csv(
        OUTPUT_DIR / "demand_calibration.csv",
        index=False
    )

    factor_df.to_csv(
        OUTPUT_DIR / "preference_calibration.csv",
        index=False
    )

    print("\nNAJLEPSZA LICZBA AGENTÓW:")
    print(best_row.to_string())

    print("\nNAJLEPSZY WSPÓŁCZYNNIK:")
    print(best_factor.to_string())

    print("\nZapisano wyniki w:", OUTPUT_DIR)


if __name__ == "__main__":
    main()

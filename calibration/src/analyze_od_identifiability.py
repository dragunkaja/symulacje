
from pathlib import Path
from itertools import product
import json
import random
import sys

import networkx as nx
import numpy as np
import pandas as pd

from pyproj import Transformer
from shapely.geometry import Point, shape

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import model_alpha as model

ZONES_PATH = ROOT / "data" / "Rejony_komunikacyjne.geojson"
CANDIDATES_PATH = ROOT / "calibration" / "results" / "processed" / "sensor_edge_candidates_alpha.csv"
OUTPUT_DIR = ROOT / "calibration" / "results" / "processed"

MIN_NODES_PER_ZONE = 10
SAMPLE_ROUTES_PER_PAIR = 500
MIN_ROUTE_LENGTH = 300
MAX_ROUTE_LENGTH = 2500
SEED = 42

SENSORS = ["Kotlarska", "Grzegórzecka"]


def load_zones(graph):
    with ZONES_PATH.open(encoding="utf-8") as file:
        data = json.load(file)

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:2178",
        always_xy=True
    )

    polygons = [
        (
            str(feature["properties"]["numer_rej"]),
            shape(feature["geometry"])
        )
        for feature in data["features"]
    ]

    zones = {}

    for node, attributes in graph.nodes(data=True):
        x, y = transformer.transform(
            float(attributes["x"]),
            float(attributes["y"])
        )

        point = Point(x, y)

        for zone_id, polygon in polygons:
            if polygon.covers(point):
                zones.setdefault(zone_id, []).append(node)
                break

    return {
        zone_id: nodes
        for zone_id, nodes in zones.items()
        if len(nodes) >= MIN_NODES_PER_ZONE
    }


def load_sensor_edges():
    candidates = pd.read_csv(
        CANDIDATES_PATH,
        dtype={"u": str, "v": str, "key": str}
    )

    candidates = candidates[
        candidates["coord_source"] == "metadane_licznikow.csv"
    ]

    sensor_edges = {
        sensor: set()
        for sensor in SENSORS
    }

    for row in candidates.itertuples(index=False):
        sensor_edges[row.sensor_name].add(
            (str(row.u), str(row.v), str(row.key))
        )

    return sensor_edges


def analyze_pair(graph, origins, destinations, sensor_edges, rng):
    candidates = list(product(origins, destinations))
    rng.shuffle(candidates)

    crossings = {
        sensor: 0
        for sensor in SENSORS
    }

    valid_routes = 0

    for origin, destination in candidates:
        try:
            route = model.find_route(
                graph,
                origin,
                destination,
                "shortest"
            )
        except nx.NetworkXNoPath:
            continue

        route_length = 0

        for u, v in zip(route, route[1:]):
            _, attributes = model.chosen_edge(
                graph,
                u,
                v,
                "shortest"
            )

            route_length += model.edge_length(attributes)

        if not MIN_ROUTE_LENGTH <= route_length <= MAX_ROUTE_LENGTH:
            continue

        crossed = set()

        for u, v in zip(route, route[1:]):
            key, _ = model.chosen_edge(
                graph,
                u,
                v,
                "shortest"
            )

            edge = (str(u), str(v), str(key))

            for sensor in SENSORS:
                if edge in sensor_edges[sensor]:
                    crossed.add(sensor)

        for sensor in crossed:
            crossings[sensor] += 1

        valid_routes += 1

        if valid_routes >= SAMPLE_ROUTES_PER_PAIR:
            break

    return {
        sensor: (
            crossings[sensor] / valid_routes
            if valid_routes > 0 else 0.0
        )
        for sensor in SENSORS
    } | {
        "valid_routes": valid_routes
    }


def main():
    graph = model.load_network(model.GRAPH_PATH)
    zones = load_zones(graph)
    sensor_edges = load_sensor_edges()

    print("\nSTREFY OD:")

    for zone_id, nodes in sorted(zones.items()):
        print(f"Rejon {zone_id}: {len(nodes)} węzłów")

    zone_ids = sorted(zones)

    od_pairs = [
        (origin, destination)
        for origin, destination in product(zone_ids, zone_ids)
        if origin != destination
    ]

    rng = random.Random(SEED)
    rows = []

    for origin, destination in od_pairs:
        probabilities = analyze_pair(
            graph,
            zones[origin],
            zones[destination],
            sensor_edges,
            rng
        )

        rows.append({
            "origin_zone": origin,
            "destination_zone": destination,
            "p_Kotlarska": probabilities["Kotlarska"],
            "p_Grzegorzecka": probabilities["Grzegórzecka"],
            "valid_routes": probabilities["valid_routes"]
        })

    results = pd.DataFrame(rows)

    matrix = results[
        ["p_Kotlarska", "p_Grzegorzecka"]
    ].to_numpy().T

    rank = np.linalg.matrix_rank(matrix)
    unknowns = matrix.shape[1]

    singular_values = np.linalg.svd(
        matrix,
        compute_uv=False
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results.to_csv(
        OUTPUT_DIR / "od_assignment_matrix.csv",
        index=False
    )

    print("\nMACIERZ PRZYPISANIA:")
    print(results.to_string(index=False))

    print("\nIDENTYFIKOWALNOŚĆ:")
    print(f"Liczba liczników: {len(SENSORS)}")
    print(f"Liczba par OD: {unknowns}")
    print(f"Wymiar macierzy A: {matrix.shape}")
    print(f"Rząd macierzy A: {rank}")
    print(f"Liczba niezidentyfikowanych wymiarów: {unknowns - rank}")
    print(f"Wartości singularne: {singular_values}")

    print("\nLICZBA POPRAWNYCH TRAS:")
    print(f"Minimum: {results['valid_routes'].min()}")
    print(f"Maksimum: {results['valid_routes'].max()}")
    print(f"Średnia: {results['valid_routes'].mean():.1f}")
    print(
        f"Pary z mniej niż {SAMPLE_ROUTES_PER_PAIR} trasami: "
        f"{(results['valid_routes'] < SAMPLE_ROUTES_PER_PAIR).sum()}"
    )

    if rank < unknowns:
        print("\nMacierz OD nie jest identyfikowalna.")
        print("Należy ograniczyć liczbę parametrów OD.")

    if (results["valid_routes"] == 0).any():
        print("\nUWAGA: Niektóre pary OD nie mają poprawnych tras.")

    print(
        "\nZapisano:",
        OUTPUT_DIR / "od_assignment_matrix.csv"
    )


if __name__ == "__main__":
    main()

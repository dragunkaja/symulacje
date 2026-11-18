"""Prototyp alfa: mikrosymulacja rowerzystów na grafie OSM.

Uruchom z katalogu głównego repozytorium:
    python src/model_alpha.py

Wymaga: networkx, plik data/raw/osm_kotlarska.graphml z notebooka.
To demonstrator, nie model skalibrowany do prawdziwych liczników.
"""

from __future__ import annotations

import csv
import heapq
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import networkx as nx

GRAPH_PATH = Path("data/raw/osm_kotlarska.graphml")
RESULTS_DIR = Path("results")
SEED = 42
N_CYCLISTS = 200  # PRZYKŁADOWA wartość, nie pochodzi z pomiarów
SIMULATION_SECONDS = 3600


@dataclass(frozen=True)
class Trip:
    origin: str
    destination: str
    start_second: int
    speed_kmh: float


def load_network(path: Path) -> nx.MultiDiGraph:
    graph = nx.read_graphml(path)
    if not graph.is_directed():
        raise ValueError("Oczekiwany jest graf skierowany OSMnx.")
    if not graph.is_multigraph():
        graph = nx.MultiDiGraph(graph)

    # Pozostawiamy tylko największą silnie spójną składową,
    # aby każda wybrana para węzłów miała możliwą trasę.
    component = max(nx.strongly_connected_components(graph), key=len)
    graph = graph.subgraph(component).copy()
    print(f"Wczytany spójny podgraf: {len(graph.nodes)} węzłów, "
          f"{len(graph.edges)} krawędzi")
    return graph


def edge_length(attributes: dict) -> float:
    return float(attributes["length"])


def edge_cost(attributes: dict, strategy: str) -> float:
    """Koszt trasy. Mnożnik 0.7 to WYŁĄCZNIE hipoteza do sprawdzenia."""
    length = edge_length(attributes)
    highway = str(attributes.get("highway", "")).lower()
    if strategy == "bike_preferred" and "cycleway" in highway:
        return 0.7 * length
    return length


def find_route(graph: nx.MultiDiGraph, origin: str,
               destination: str, strategy: str) -> list[str]:
    if strategy not in {"shortest", "bike_preferred"}:
        raise ValueError("Nieznana strategia")

    # MultiDiGraph może mieć kilka równoległych krawędzi u -> v.
    def weight(u: str, v: str, alternatives: dict) -> float:
        return min(edge_cost(attrs, strategy) for attrs in alternatives.values())

    return nx.shortest_path(graph, origin, destination, weight=weight)


def chosen_edge(graph: nx.MultiDiGraph, u: str, v: str,
                strategy: str) -> tuple[str, dict]:
    return min(graph[u][v].items(), key=lambda item: edge_cost(item[1], strategy))


def draw_trips(graph: nx.MultiDiGraph, count: int,
               seed: int = SEED) -> list[Trip]:
    """Losowe OD = dane SYNTETYCZNE. Docelowo zastąpić rozkładem OD."""
    rng = random.Random(seed)
    nodes = list(graph.nodes)
    trips: list[Trip] = []
    attempts = 0

    while len(trips) < count and attempts < count * 50:
        attempts += 1
        origin, destination = rng.sample(nodes, 2)
        route = find_route(graph, origin, destination, "shortest")
        length = sum(edge_length(chosen_edge(graph, u, v, "shortest")[1])
                     for u, v in zip(route, route[1:]))
        if not 300 <= length <= 2500:
            continue
        trips.append(Trip(
            origin=origin,
            destination=destination,
            start_second=rng.randrange(0, 2400),
            speed_kmh=rng.uniform(12, 18),  # założenie demonstracyjne
        ))

    if len(trips) < count:
        raise ValueError("Za mało tras o zadanej długości: zmień progi w draw_trips.")
    return trips


def simulate(graph: nx.MultiDiGraph, trips: list[Trip], strategy: str,
             horizon: int = SIMULATION_SECONDS) -> tuple[Counter, list[float]]:
    """Zdarzenia: rowerzysta wjeżdża na kolejny odcinek swojej trasy."""
    routes = [find_route(graph, trip.origin, trip.destination, strategy)
              for trip in trips]
    queue = [(trip.start_second, idx, 0) for idx, trip in enumerate(trips)]
    heapq.heapify(queue)
    crossings: Counter = Counter()
    durations: list[float] = []

    while queue:
        time, cyclist_id, segment_idx = heapq.heappop(queue)
        trip = trips[cyclist_id]
        route = routes[cyclist_id]
        if segment_idx == len(route) - 1:
            durations.append(time - trip.start_second)
            continue

        u, v = route[segment_idx], route[segment_idx + 1]
        key, attributes = chosen_edge(graph, u, v, strategy)
        travel_seconds = edge_length(attributes) / (trip.speed_kmh / 3.6)

        # Liczymy przejazd przez ŚRODEK odcinka, nie jego początek.
        if time + travel_seconds / 2 < horizon:
            crossings[(u, v, key)] += 1

        heapq.heappush(queue, (time + travel_seconds, cyclist_id, segment_idx + 1))

    return crossings, durations


def save_edge_counts(path: Path, crossings: Counter) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["u", "v", "key", "simulated_passages"])
        for (u, v, key), count in crossings.most_common():
            writer.writerow([u, v, key, count])


def main() -> None:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"Brak {GRAPH_PATH}. Najpierw uruchom notebook 01_environment_data.ipynb "
            "i zapisz graf do data/raw/.")

    graph = load_network(GRAPH_PATH)
    trips = draw_trips(graph, N_CYCLISTS)
    for strategy in ("shortest", "bike_preferred"):
        counts, durations = simulate(graph, trips, strategy)
        save_edge_counts(RESULTS_DIR / f"alpha_{strategy}.csv", counts)
        print(f"{strategy}: ukończono {len(durations)} podróży, "
              f"średni czas = {sum(durations) / len(durations) / 60:.2f} min, "
              f"odcinków z ruchem = {len(counts)}")

    print("Wyniki zapisano w results/. To NIE jest jeszcze kalibracja z licznikami.")


if __name__ == "__main__":
    main()

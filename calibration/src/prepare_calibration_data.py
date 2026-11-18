from __future__ import annotations

import ast
from pathlib import Path

import networkx as nx
import pandas as pd
from pyproj import Transformer
from shapely import wkt
from shapely.geometry import LineString, Point
from shapely.ops import transform

REPO_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = REPO_ROOT / "data"
RESULTS_DIR = CALIBRATION_DIR / "results" / "processed"

GRAPH_PATH = DATA_DIR / "raw" / "osm_kotlarska.graphml"
DAILY_PATH = DATA_DIR / "Liczniki-dzienne.csv"
METADATA_PATH = DATA_DIR / "metadane_licznikow.csv"
ALTERNATE_COORDS_PATH = DATA_DIR / "wspolrzedne_licznikow.csv"
MONTHLY_PATH = DATA_DIR / "wszystkie_dane_miesieczne.csv"
SENSORS = ["Kotlarska", "Grzegórzecka"]
TIE_TOLERANCE_M = 0.75


def load_edge_geometries(graph: nx.MultiDiGraph, transformer: Transformer):
    edges = []
    for u, v, key, attributes in graph.edges(keys=True, data=True):
        geometry_value = attributes.get("geometry")
        if geometry_value:
            geometry = wkt.loads(geometry_value)
        else:
            node_u = graph.nodes[u]
            node_v = graph.nodes[v]
            geometry = LineString([
                (float(node_u["x"]), float(node_u["y"])),
                (float(node_v["x"]), float(node_v["y"])),
            ])
        geometry_metric = transform(transformer.transform, geometry)
        edges.append((str(u), str(v), str(key), attributes, geometry_metric))
    return edges


def load_sensor_coordinates():
    metadata = pd.read_csv(METADATA_PATH)
    metadata = metadata[metadata["name"].isin(SENSORS)].copy()
    metadata["coord_source"] = "metadane_licznikow.csv"

    alternate = pd.read_csv(ALTERNATE_COORDS_PATH, sep=";")
    alternate["Licznik"] = alternate["Licznik"].replace({"Gregorzecka": "Grzegórzecka"})
    alternate = alternate[alternate["Licznik"].isin(SENSORS)].copy()
    alternate = alternate.rename(columns={"Licznik": "name", "lon": "longitude", "lat": "latitude"})
    alternate["coord_source"] = "wspolrzedne_licznikow.csv"
    alternate["id"] = alternate["name"].str.lower()

    metadata = metadata.rename(columns={"lon": "longitude", "lat": "latitude"})
    columns = ["id", "name", "longitude", "latitude", "coord_source"]
    return pd.concat([metadata[columns], alternate[columns]], ignore_index=True)


def match_sensor_edges(graph, edge_geometries, coordinates, transformer):
    largest_component = set(max(nx.strongly_connected_components(graph), key=len))
    rows = []

    for sensor in coordinates.itertuples(index=False):
        point = Point(transformer.transform(sensor.longitude, sensor.latitude))
        distances = [geometry.distance(point) for *_, geometry in edge_geometries]
        minimum_distance = min(distances)

        candidates = [
            edge
            for edge, distance in zip(edge_geometries, distances)
            if distance <= minimum_distance + TIE_TOLERANCE_M
        ]
        candidates.sort(key=lambda edge: (edge[0], edge[1], edge[2]))

        for rank, (u, v, key, attributes, _) in enumerate(candidates, start=1):
            rows.append({
                "sensor_id": sensor.id,
                "sensor_name": sensor.name,
                "coord_source": sensor.coord_source,
                "longitude": sensor.longitude,
                "latitude": sensor.latitude,
                "candidate_rank": rank,
                "distance_m": round(minimum_distance, 2),
                "u": u,
                "v": v,
                "key": key,
                "highway": str(attributes.get("highway", "")),
                "name": str(attributes.get("name", "")),
                "length_m": float(attributes.get("length", 0)),
                "in_largest_scc": u in largest_component and v in largest_component,
                "confirmed": False,
            })

    return pd.DataFrame(rows)


def prepare_daily_reference():
    daily = pd.read_csv(DAILY_PATH, parse_dates=["Date"])
    for sensor in SENSORS:
        daily[sensor] = pd.to_numeric(daily[sensor], errors="coerce")

    common = daily[["Date", *SENSORS]].dropna().copy()
    common["day_type"] = common["Date"].dt.dayofweek.map(
        lambda day: "weekday" if day < 5 else "weekend"
    )

    summary = []
    for sensor in SENSORS:
        values = common[sensor]
        summary.append({
            "sensor": sensor,
            "valid_days_in_common_period": len(common),
            "first_date": common["Date"].min().date(),
            "last_date": common["Date"].max().date(),
            "mean_daily_count": round(values.mean(), 2),
            "median_daily_count": round(values.median(), 2),
            "zero_days": int((values == 0).sum()),
        })

    return common, pd.DataFrame(summary)


def prepare_hourly_reference():
    monthly = pd.read_csv(MONTHLY_PATH)
    rows = []

    for record in monthly.itertuples(index=False):
        values = record._asdict()
        for sensor_id, sensor_name in [("kotlarska", "Kotlarska"), ("grzegorzecka", "Grzegórzecka")]:
            profile = ast.literal_eval(values[sensor_id])
            for day_type, field in [("weekday", "hourly_weekday"), ("weekend", "hourly_weekend")]:
                for hour_data in profile.get(field, []):
                    rows.append({
                        "sensor": sensor_name,
                        "year": int(values["rok"]),
                        "month": int(values["miesiac"]),
                        "day_type": day_type,
                        "hour": int(hour_data["hour"]),
                        "avg": float(hour_data["avg"]),
                        "median": float(hour_data["median"]),
                        "min": float(hour_data["min"]),
                        "max": float(hour_data["max"]),
                    })

    return pd.DataFrame(rows)


def main():
    graph = nx.read_graphml(GRAPH_PATH)
    if not graph.is_directed():
        raise ValueError("Graf musi być skierowany.")
    if not graph.is_multigraph():
        graph = nx.MultiDiGraph(graph)

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2180", always_xy=True)
    coordinates = load_sensor_coordinates()
    edge_geometries = load_edge_geometries(graph, transformer)
    candidates = match_sensor_edges(graph, edge_geometries, coordinates, transformer)
    daily, daily_summary = prepare_daily_reference()
    hourly = prepare_hourly_reference()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    candidates.to_csv(RESULTS_DIR / "sensor_edge_candidates_alpha.csv", index=False)
    daily.to_csv(RESULTS_DIR / "calibration_daily_reference.csv", index=False)
    daily_summary.to_csv(RESULTS_DIR / "calibration_daily_summary.csv", index=False)
    hourly.to_csv(RESULTS_DIR / "calibration_hourly_reference.csv", index=False)

    print(f"Graf: {len(graph.nodes)} węzłów, {len(graph.edges)} skierowanych krawędzi")
    print("\nWspólny okres danych dziennych:")
    print(daily_summary.to_string(index=False))
    print("\nNajbliższe krawędzie dla liczników:")
    print(
        candidates.groupby(["sensor_name", "coord_source"], as_index=False)
        .agg(distance_m=("distance_m", "first"),
             candidate_edges=("candidate_rank", "count"),
             all_candidates_in_largest_scc=("in_largest_scc", "all"))
        .to_string(index=False)
    )
    print("\nProfile godzinowe:")
    print(
        hourly.groupby(["sensor", "day_type"])
        .agg(months=("month", "count"), hours=("hour", "nunique"))
        .to_string()
    )
    print(f"\nWyniki zapisano w: {RESULTS_DIR}")
    print("Mapowania krawędzi są kandydatami i wymagają potwierdzenia na mapie.")


if __name__ == "__main__":
    main()

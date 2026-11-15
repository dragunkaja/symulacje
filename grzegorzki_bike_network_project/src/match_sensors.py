import pandas as pd
import osmnx as ox

from .config import (
    METRIC_CRS,
    MAX_SENSOR_DISTANCE_M,
    CANDIDATE_TIE_TOLERANCE_M,
    PROCESSED_DIR,
)
from .common import load_graph, read_sensors_gdf, csv_safe

def match_sensors():
    """
    Find nearest directed edge(s) for each sensor.
    This creates candidates only: it does NOT silently confirm a match.
    """
    G = load_graph()
    _, edges = ox.graph_to_gdfs(
        G,
        nodes=True,
        edges=True,
        node_geometry=True,
        fill_edge_geometry=True,
    )

    edges = edges.reset_index()
    edges_metric = edges.to_crs(METRIC_CRS)
    sensors_metric = read_sensors_gdf().to_crs(METRIC_CRS)

    candidate_rows = []
    summary_rows = []

    for _, sensor in sensors_metric.iterrows():
        distances = edges_metric.geometry.distance(sensor.geometry)
        if distances.empty or distances.isna().all():
            raise RuntimeError("No usable edge geometries found in the graph.")

        min_distance = float(distances.min())
        mask = distances <= min_distance + CANDIDATE_TIE_TOLERANCE_M
        nearest = edges_metric.loc[mask].copy()
        nearest["distance_m"] = distances.loc[mask].astype(float)
        nearest = nearest.sort_values(
            ["distance_m", "u", "v", "key"]
        )

        if min_distance <= MAX_SENSOR_DISTANCE_M:
            status = "REVIEW_ON_MAP"
        else:
            status = "CHECK_COORDINATE_OR_NETWORK"

        summary_rows.append({
            "sensor_id": sensor["sensor_id"],
            "nearest_distance_m": round(min_distance, 2),
            "candidate_count": len(nearest),
            "status": status,
        })

        for rank, (_, edge) in enumerate(nearest.iterrows(), start=1):
            candidate_rows.append({
                "sensor_id": sensor["sensor_id"],
                "candidate_rank": rank,
                "distance_m": round(float(edge["distance_m"]), 2),
                "u": str(edge["u"]),
                "v": str(edge["v"]),
                "key": str(edge["key"]),
                "osmid": csv_safe(edge.get("osmid")),
                "name": csv_safe(edge.get("name")),
                "highway": csv_safe(edge.get("highway")),
                "oneway": csv_safe(edge.get("oneway")),
                "access": csv_safe(edge.get("access")),
                "bicycle": csv_safe(edge.get("bicycle")),
                "cycleway": csv_safe(edge.get("cycleway")),
                "surface": csv_safe(edge.get("surface")),
                "direction": "unknown",
                "use_in_model": False,
                "confirmed": False,
                "status": status,
            })

    candidates = pd.DataFrame(candidate_rows)
    summary = pd.DataFrame(summary_rows)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    candidates.to_csv(
        PROCESSED_DIR / "sensor_edge_candidates.csv",
        index=False,
        encoding="utf-8-sig",
    )
    summary.to_csv(
        PROCESSED_DIR / "sensor_match_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Editable template: inspect candidates on the map, then set
    # use_in_model=True, confirmed=True and direction appropriately.
    candidates.to_csv(
        PROCESSED_DIR / "sensor_edge_map_template.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nNearest-edge summary:")
    print(summary.to_string(index=False))
    print("\nIMPORTANT: candidates are suggestions, not confirmed sensor locations.")
    print(f"Files saved in: {PROCESSED_DIR}")

    return candidates, summary

if __name__ == "__main__":
    match_sensors()

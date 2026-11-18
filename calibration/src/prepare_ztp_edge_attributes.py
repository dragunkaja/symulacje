
from pathlib import Path
import json

import networkx as nx
from pyproj import Transformer
from shapely import wkt
from shapely.geometry import LineString, shape
from shapely.ops import transform, unary_union

ROOT = Path(__file__).resolve().parents[2]

GRAPH_PATH = ROOT / "data" / "raw" / "osm_kotlarska.graphml"
ZTP_PATH = ROOT / "data" / "raw" / "cycleways_kotlarska.geojson"
OUTPUT_PATH = ROOT / "data" / "processed" / "osm_kotlarska_ztp.graphml"

BUFFER_M = 1.5
MIN_OVERLAP_RATIO = 0.5

PREFERRED_TYPES = {
    "droga rowerowa",
    "ciąg pieszo-rowerowy",
    "kontraruch",
    "kontrapas",
    "przejazd",
}

SENSORS = {
    "Kotlarska": ("595413007", "595413013"),
    "Grzegórzecka": ("3797258848", "595413024"),
}


def main():
    graph = nx.read_graphml(GRAPH_PATH)

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:2180",
        always_xy=True
    )

    with ZTP_PATH.open(encoding="utf-8") as file:
        geojson = json.load(file)

    ztp_geometries = []

    for feature in geojson["features"]:
        properties = feature["properties"]

        if properties.get("rodzaj") in PREFERRED_TYPES:
            geometry = shape(feature["geometry"])
            geometry = transform(transformer.transform, geometry)
            ztp_geometries.append(geometry)

    if not ztp_geometries:
        raise ValueError("Nie znaleziono infrastruktury rowerowej ZTP.")

    ztp_area = unary_union(ztp_geometries).buffer(BUFFER_M)

    marked_edges = 0

    for u, v, key, attributes in graph.edges(
        keys=True,
        data=True
    ):
        geometry_value = attributes.get("geometry")

        if geometry_value:
            geometry = wkt.loads(str(geometry_value))
        else:
            geometry = LineString([
                (
                    float(graph.nodes[u]["x"]),
                    float(graph.nodes[u]["y"])
                ),
                (
                    float(graph.nodes[v]["x"]),
                    float(graph.nodes[v]["y"])
                )
            ])

        geometry = transform(transformer.transform, geometry)

        if geometry.length == 0:
            ratio = 0.0
        else:
            ratio = geometry.intersection(ztp_area).length / geometry.length

        is_bike_infrastructure = ratio >= MIN_OVERLAP_RATIO

        attributes["ztp_bike_overlap_ratio"] = round(ratio, 4)
        attributes["ztp_bike_infrastructure"] = (
            "yes" if is_bike_infrastructure else "no"
        )

        if is_bike_infrastructure:
            marked_edges += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(graph, OUTPUT_PATH)

    print(f"Węzły: {len(graph.nodes)}")
    print(f"Krawędzie: {len(graph.edges)}")
    print(f"Krawędzie oznaczone przez ZTP: {marked_edges}")
    print("\nKontrola liczników:")

    for sensor, (u, v) in SENSORS.items():
        for a, b in [(u, v), (v, u)]:
            for key, attributes in graph[a][b].items():
                print(
                    sensor,
                    f"{a} -> {b}",
                    f"OSM={attributes.get('highway')}",
                    f"ZTP={attributes['ztp_bike_infrastructure']}",
                    f"overlap={attributes['ztp_bike_overlap_ratio']}"
                )

    print(f"\nZapisano: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

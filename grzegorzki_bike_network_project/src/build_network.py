from pathlib import Path
import networkx as nx
import geopandas as gpd
import osmnx as ox

from .config import (
    NETWORK_SOURCE,
    NETWORK_TYPE,
    BUFFER_M,
    METRIC_CRS,
    GEOGRAPHIC_CRS,
    EXTRA_WAY_TAGS,
    REFERENCE_CYCLIST_SPEED_KMH,
    GRAPH_FILE,
    EXISTING_GRAPH_FILE,
    PROCESSED_DIR,
)
from .common import read_sensors_gdf, tag_values

FORBIDDEN_ACCESS = {"no", "private", "customers", "permit"}
BICYCLE_ALLOWED = {"yes", "designated", "permissive", "official"}

def make_study_polygon():
    """
    Build one study polygon around all six sensors:
    convex hull of sensor points + 1 km buffer.
    Distances/buffer are calculated in EPSG:2180 (metres).
    """
    sensors_metric = read_sensors_gdf().to_crs(METRIC_CRS)
    hull = sensors_metric.geometry.unary_union.convex_hull
    buffered_hull = hull.buffer(BUFFER_M)

    polygon_wgs84 = gpd.GeoSeries(
        [buffered_hull], crs=METRIC_CRS
    ).to_crs(GEOGRAPHIC_CRS).iloc[0]

    return polygon_wgs84, buffered_hull

def configure_osmnx():
    """Keep useful OSM attributes needed by later route-choice models."""
    ox.settings.use_cache = True
    ox.settings.log_console = True
    ox.settings.timeout = 180

    current = list(ox.settings.useful_tags_way)
    ox.settings.useful_tags_way = list(dict.fromkeys(current + EXTRA_WAY_TAGS))

def bicycle_access_is_forbidden(data):
    """
    Conservative post-filter:
    - always remove bicycle=no;
    - remove general access=no/private/customers/permit unless
      an explicit bicycle=yes/designated/permissive/official overrides it.
    OSMnx's network_type='bike' filter is applied before this step as well.
    """
    bicycle = set(tag_values(data.get("bicycle")))
    access = set(tag_values(data.get("access")))
    highway = set(tag_values(data.get("highway")))

    if "no" in bicycle:
        return True

    explicit_bicycle_permission = bool(bicycle & BICYCLE_ALLOWED)

    if access & FORBIDDEN_ACCESS and not explicit_bicycle_permission:
        return True

    # Motorways are excluded unless OSM explicitly permits bicycles.
    if highway & {"motorway", "motorway_link"} and not explicit_bicycle_permission:
        return True

    return False

def add_model_attributes(G):
    """Add stable, simulation-friendly attributes to every directed edge."""
    speed_m_per_s = REFERENCE_CYCLIST_SPEED_KMH * 1000 / 3600

    edges_to_remove = []
    for u, v, key, data in G.edges(keys=True, data=True):
        if bicycle_access_is_forbidden(data):
            edges_to_remove.append((u, v, key))
            continue

        length_m = float(data.get("length", 0.0))
        data["length_m"] = length_m
        data["edge_id"] = f"{u}|{v}|{key}"

        # Reference only. Each future agent can calculate its own travel time
        # from length_m and its own speed_kmh.
        data["reference_travel_time_s_15kmh"] = (
            length_m / speed_m_per_s if speed_m_per_s > 0 else 0.0
        )

    for u, v, key in edges_to_remove:
        G.remove_edge(u, v, key)

    # Remove nodes left without any incoming or outgoing edge.
    isolated = list(nx.isolates(G))
    if isolated:
        G.remove_nodes_from(isolated)

    G.graph["network_type"] = NETWORK_TYPE
    G.graph["study_area_buffer_m"] = BUFFER_M
    G.graph["metric_crs_for_analysis"] = METRIC_CRS
    G.graph["bicycle_access_filter_applied"] = True

    return G

def export_graph_layers(G):
    """Export graph nodes and edges as separate GeoPackage files."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    nodes, edges = ox.graph_to_gdfs(
        G,
        nodes=True,
        edges=True,
        node_geometry=True,
        fill_edge_geometry=True,
    )

    def make_gpkg_safe(gdf):
        gdf = gdf.copy()
        for col in gdf.columns:
            if col == "geometry":
                continue
            gdf[col] = gdf[col].map(
                lambda x: "|".join(map(str, x))
                if isinstance(x, (list, tuple, set)) else x
            )
        return gdf

    nodes_out = make_gpkg_safe(nodes.reset_index())
    edges_out = make_gpkg_safe(edges.reset_index())

    nodes_path = PROCESSED_DIR / "network_nodes.gpkg"
    edges_path = PROCESSED_DIR / "network_edges.gpkg"

    if nodes_path.exists():
        nodes_path.unlink()
    if edges_path.exists():
        edges_path.unlink()

    nodes_out.to_file(nodes_path, layer="nodes", driver="GPKG")
    edges_out.to_file(edges_path, layer="edges", driver="GPKG")

def build_network():
    """Load the uploaded graph or download a fresh bike network from OSM."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if NETWORK_SOURCE == "existing":
        if not Path(EXISTING_GRAPH_FILE).exists():
            raise FileNotFoundError(EXISTING_GRAPH_FILE)
        print(f"Loading existing graph: {EXISTING_GRAPH_FILE}")
        G = ox.load_graphml(filepath=EXISTING_GRAPH_FILE)

    elif NETWORK_SOURCE == "download":
        configure_osmnx()
        polygon, buffered_hull = make_study_polygon()

        print("Downloading bicycle network from OpenStreetMap...")
        print(f"Network type: {NETWORK_TYPE}")
        print(f"Study area buffer: {BUFFER_M} m")

        G = ox.graph_from_polygon(
            polygon,
            network_type=NETWORK_TYPE,
            simplify=True,
            retain_all=True,
            truncate_by_edge=True,
        )

    else:
        raise ValueError(
            "NETWORK_SOURCE must be either 'download' or 'existing'."
        )

    G = add_model_attributes(G)

    if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
        raise RuntimeError("The resulting graph is empty.")

    ox.save_graphml(G, filepath=GRAPH_FILE)
    export_graph_layers(G)

    print(f"Saved GraphML: {GRAPH_FILE}")
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Directed edges: {G.number_of_edges()}")
    print("Saved GeoPackage node and edge layers.")

    return G

if __name__ == "__main__":
    build_network()

import json
import matplotlib.pyplot as plt
import geopandas as gpd
import osmnx as ox
import folium

from .config import (
    OUTPUT_DIR,
    GEOGRAPHIC_CRS,
)
from .common import load_graph, read_sensors_gdf, tag_values

def visualize_graph():
    G = load_graph()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    nodes, edges = ox.graph_to_gdfs(
        G,
        nodes=True,
        edges=True,
        node_geometry=True,
        fill_edge_geometry=True,
    )

    edges_wgs = edges.to_crs(GEOGRAPHIC_CRS)
    sensors_wgs = read_sensors_gdf().to_crs(GEOGRAPHIC_CRS)

    # ---------- Static PNG ----------
    fig, ax = plt.subplots(figsize=(13, 12))

    # General bicycle-accessible network.
    edges_wgs.plot(
        ax=ax,
        color="#a0a0a0",
        linewidth=0.45,
        alpha=0.8,
        zorder=1,
    )

    # Highlight mapped cycleways and paths.
    highlight_mask = edges_wgs["highway"].apply(
        lambda value: bool(
            set(tag_values(value)) & {"cycleway", "path"}
        )
    )
    if highlight_mask.any():
        edges_wgs.loc[highlight_mask].plot(
            ax=ax,
            color="#25855a",
            linewidth=1.0,
            alpha=0.95,
            zorder=2,
        )

    sensors_wgs.plot(
        ax=ax,
        color="#d62728",
        edgecolor="white",
        linewidth=0.8,
        markersize=65,
        zorder=5,
    )

    for _, sensor in sensors_wgs.iterrows():
        ax.annotate(
            sensor["sensor_id"],
            (sensor.geometry.x, sensor.geometry.y),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
            zorder=6,
        )

    ax.set_title("Grzegórzki – sieć rowerowa i liczniki")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.15)

    png_path = OUTPUT_DIR / "network_overview.png"
    fig.savefig(png_path, dpi=220, bbox_inches="tight")
    plt.close(fig)

    # ---------- Interactive HTML map ----------
    center_lat = float(sensors_wgs["latitude"].mean())
    center_lon = float(sensors_wgs["longitude"].mean())

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=14,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    edge_geojson = json.loads(edges_wgs.reset_index().to_json())

    folium.GeoJson(
        edge_geojson,
        name="Sieć dostępna dla rowerów",
        style_function=lambda feature: {
            "color": (
                "#25855a"
                if set(tag_values(feature["properties"].get("highway")))
                   & {"cycleway", "path"}
                else "#777777"
            ),
            "weight": 2,
            "opacity": 0.75,
        },
    ).add_to(m)

    for _, sensor in sensors_wgs.iterrows():
        folium.Marker(
            location=[float(sensor["latitude"]), float(sensor["longitude"])],
            tooltip=sensor["sensor_id"],
            popup=(
                f'{sensor["sensor_id"]}<br>'
                f'lat: {sensor["latitude"]}<br>'
                f'lon: {sensor["longitude"]}'
            ),
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    folium.LayerControl().add_to(m)

    html_path = OUTPUT_DIR / "network_map.html"
    m.save(str(html_path))

    print(f"Static map: {png_path}")
    print(f"Interactive map: {html_path}")
    return png_path, html_path

if __name__ == "__main__":
    visualize_graph()

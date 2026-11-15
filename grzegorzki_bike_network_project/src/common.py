from pathlib import Path
import pandas as pd
import geopandas as gpd
import osmnx as ox

from .config import (
    SENSORS_CSV,
    GRAPH_FILE,
    GEOGRAPHIC_CRS,
)

def read_sensors_table() -> pd.DataFrame:
    """Read and validate the user-provided sensor coordinates."""
    df = pd.read_csv(SENSORS_CSV, sep=";", encoding="utf-8")

    required = {"sensor_id", "latitude", "longitude"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {SENSORS_CSV}: {sorted(missing)}")

    df = df.copy()
    df["sensor_id"] = df["sensor_id"].astype(str).str.strip()
    df["latitude"] = pd.to_numeric(df["latitude"], errors="raise")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="raise")

    if df["sensor_id"].duplicated().any():
        duplicated = df.loc[df["sensor_id"].duplicated(), "sensor_id"].tolist()
        raise ValueError(f"Duplicate sensor_id values: {duplicated}")

    if not df["latitude"].between(-90, 90).all():
        raise ValueError("Latitude values must be between -90 and 90.")
    if not df["longitude"].between(-180, 180).all():
        raise ValueError("Longitude values must be between -180 and 180.")

    return df

def read_sensors_gdf() -> gpd.GeoDataFrame:
    """Create WGS84 point geometries from the sensor table."""
    df = read_sensors_table()
    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=GEOGRAPHIC_CRS,
    )

def load_graph():
    """Load the prepared OSMnx GraphML file."""
    if not Path(GRAPH_FILE).exists():
        raise FileNotFoundError(
            f"Graph not found: {GRAPH_FILE}. Run build_network.py first."
        )
    return ox.load_graphml(filepath=GRAPH_FILE)

def tag_values(value):
    """Normalize OSM tag values that may be strings or lists."""
    import ast

    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(v).strip().lower() for v in value]

    text = str(value).strip()
    if not text:
        return []

    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, (list, tuple, set)):
                return [str(v).strip().lower() for v in parsed]
        except (ValueError, SyntaxError):
            pass

    return [text.lower()]

def csv_safe(value):
    """Convert list-like OSM attributes into readable CSV text."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return "|".join(str(v) for v in value)
    return str(value)

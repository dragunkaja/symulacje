from pathlib import Path

# Project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR = PROJECT_DIR / "outputs"

SENSORS_CSV = PROJECT_DIR / "sensors.csv"
EXISTING_GRAPH_FILE = RAW_DIR / "network_existing.graphml"
GRAPH_FILE = PROCESSED_DIR / "network.graphml"

# "download" = build a fresh bicycle network from OpenStreetMap.
# "existing" = inspect/use the uploaded GraphML as-is (not recommended
# for the first final model because some sensors are far from its edges).
NETWORK_SOURCE = "download"

# OSMnx network filter: bicycle-accessible network according to OSM tags.
NETWORK_TYPE = "bike"

# The polygon is the convex hull of all sensor points, buffered by this distance.
BUFFER_M = 1000

# Metric CRS used only for distances, buffers and spatial matching.
METRIC_CRS = "EPSG:2180"
GEOGRAPHIC_CRS = "EPSG:4326"

# Matching is a candidate-generation step, not automatic confirmation.
# Any sensor farther away than this must be checked manually.
MAX_SENSOR_DISTANCE_M = 30.0

# Include equally-near directed edges (e.g. reverse directions) in the candidate list.
CANDIDATE_TIE_TOLERANCE_M = 0.75

# Baseline value for a reference travel-time attribute only.
# Later each agent will calculate travel time using its own speed.
REFERENCE_CYCLIST_SPEED_KMH = 15.0

# OSM tags worth retaining for later route choice and network analysis.
EXTRA_WAY_TAGS = [
    "bicycle",
    "cycleway",
    "cycleway:left",
    "cycleway:right",
    "cycleway:both",
    "surface",
    "smoothness",
    "lit",
    "segregated",
    "tracktype",
    "access",
    "service",
    "maxspeed",
    "lanes",
    "width",
    "bridge",
    "tunnel",
    "junction",
    "foot",
    "motor_vehicle",
]

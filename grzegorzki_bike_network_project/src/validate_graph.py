from pathlib import Path
import networkx as nx
import pandas as pd
import osmnx as ox

from .config import (
    PROCESSED_DIR,
    MAX_SENSOR_DISTANCE_M,
)
from .common import load_graph, tag_values

def validate_graph():
    G = load_graph()

    lines = []
    lines.append("GRAPH VALIDATION REPORT")
    lines.append("=======================")
    lines.append(f"Graph type: {type(G).__name__}")
    lines.append(f"Directed: {G.is_directed()}")
    lines.append(f"Multigraph: {G.is_multigraph()}")
    lines.append(f"Nodes: {G.number_of_nodes()}")
    lines.append(f"Directed edges: {G.number_of_edges()}")

    weak_components = list(nx.weakly_connected_components(G))
    strong_components = list(nx.strongly_connected_components(G))
    largest_weak = max((len(c) for c in weak_components), default=0)
    largest_strong = max((len(c) for c in strong_components), default=0)

    lines.append(f"Weakly connected components: {len(weak_components)}")
    lines.append(f"Largest weak component: {largest_weak} nodes")
    lines.append(f"Strongly connected components: {len(strong_components)}")
    lines.append(f"Largest strong component: {largest_strong} nodes")

    missing_length = 0
    nonpositive_length = 0
    access_no = 0
    bicycle_no = 0

    for _, _, _, data in G.edges(keys=True, data=True):
        length = data.get("length_m", data.get("length"))
        if length is None:
            missing_length += 1
        else:
            try:
                if float(length) <= 0:
                    nonpositive_length += 1
            except (TypeError, ValueError):
                missing_length += 1

        if "no" in tag_values(data.get("access")):
            access_no += 1
        if "no" in tag_values(data.get("bicycle")):
            bicycle_no += 1

    lines.append(f"Edges missing length: {missing_length}")
    lines.append(f"Edges with non-positive length: {nonpositive_length}")
    lines.append(f"Edges tagged access=no: {access_no}")
    lines.append(f"Edges tagged bicycle=no: {bicycle_no}")

    candidates_path = PROCESSED_DIR / "sensor_edge_candidates.csv"
    if candidates_path.exists():
        candidates = pd.read_csv(candidates_path, dtype={"u": str, "v": str, "key": str})
        summary = (
            candidates.groupby("sensor_id", as_index=False)["distance_m"]
            .min()
            .rename(columns={"distance_m": "nearest_distance_m"})
        )

        lines.append("")
        lines.append("SENSOR DISTANCES")
        lines.append("----------------")
        for _, row in summary.iterrows():
            status = (
                "OK - inspect on map"
                if row["nearest_distance_m"] <= MAX_SENSOR_DISTANCE_M
                else "WARNING - check coordinate/network"
            )
            lines.append(
                f'{row["sensor_id"]}: {row["nearest_distance_m"]:.2f} m; {status}'
            )

        # Provisional directed reachability between sensor candidate edges.
        # For a source edge u->v, a route can continue from v.
        # For a destination edge u->v, a route can arrive at u.
        matrix_rows = []
        grouped = {
            sid: group
            for sid, group in candidates.groupby("sensor_id")
        }
        sensor_ids = list(grouped.keys())

        for source_id in sensor_ids:
            row = {"source_sensor": source_id}
            source_group = grouped[source_id]
            for target_id in sensor_ids:
                if source_id == target_id:
                    row[target_id] = True
                    continue

                target_group = grouped[target_id]
                reachable = False

                for _, source_edge in source_group.iterrows():
                    for _, target_edge in target_group.iterrows():
                        try:
                            if nx.has_path(
                                G,
                                str(source_edge["v"]),
                                str(target_edge["u"]),
                            ):
                                reachable = True
                                break
                        except (nx.NodeNotFound, nx.NetworkXError):
                            continue
                    if reachable:
                        break

                row[target_id] = reachable

            matrix_rows.append(row)

        pd.DataFrame(matrix_rows).to_csv(
            PROCESSED_DIR / "sensor_reachability.csv",
            index=False,
            encoding="utf-8-sig",
        )
        lines.append("")
        lines.append(
            "Directed reachability matrix saved to sensor_reachability.csv."
        )
        lines.append(
            "Reachability is provisional until sensor-edge candidates are manually confirmed."
        )
    else:
        lines.append("")
        lines.append("Sensor candidates not found. Run match_sensors.py first.")

    report = "\n".join(lines)
    report_path = PROCESSED_DIR / "validation_report.txt"
    report_path.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nReport saved: {report_path}")

    return report

if __name__ == "__main__":
    validate_graph()

import osmnx as ox

G = ox.graph_from_place(
    "Grzegórzki, Kraków, Poland",
    network_type="bike",
    simplify=True,
    retain_all=True
)

ox.save_graphml(
    G,
    "network.graphml"
)
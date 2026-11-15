from src.build_network import build_network
from src.match_sensors import match_sensors
from src.validate_graph import validate_graph
from src.visualize_graph import visualize_graph

def main():
    print("\n[1/4] BUILD NETWORK")
    build_network()

    print("\n[2/4] MATCH SENSORS TO EDGE CANDIDATES")
    match_sensors()

    print("\n[3/4] VALIDATE GRAPH")
    validate_graph()

    print("\n[4/4] VISUALIZE GRAPH")
    visualize_graph()

    print("\nPipeline finished.")
    print("Check the outputs/ and data/processed/ folders.")

if __name__ == "__main__":
    main()

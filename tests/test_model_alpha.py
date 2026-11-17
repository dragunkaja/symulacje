"""Testy prototypu: python -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from model_alpha import Trip, edge_cost, find_route, simulate


class ModelAlphaTests(unittest.TestCase):
    def setUp(self):
        self.g = nx.MultiDiGraph()
        self.g.add_edge("A", "B", length=100, highway="residential")
        self.g.add_edge("B", "C", length=100, highway="residential")
        self.g.add_edge("A", "C", length=250, highway="cycleway")

    def test_length_weight(self):
        self.assertEqual(find_route(self.g, "A", "C", "shortest"), ["A", "B", "C"])

    def test_bike_preference(self):
        self.assertEqual(find_route(self.g, "A", "C", "bike_preferred"), ["A", "C"])

    def test_count_passage(self):
        trips = [Trip("A", "C", 0, 18)]
        counts, times = simulate(self.g, trips, "shortest", horizon=3600)
        self.assertEqual(sum(counts.values()), 2)
        self.assertEqual(len(times), 1)
        self.assertAlmostEqual(times[0], 40.0)

    def test_cost(self):
        self.assertEqual(edge_cost({"length": 100, "highway": "cycleway"}, "bike_preferred"), 70)


if __name__ == "__main__":
    unittest.main()

import unittest
import random
from src.data import node_data
import networkx as nx
from timeit import default_timer as timer
import time
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCaseForComparison(unittest.TestCase):
    def test_time_dijkstra_my(self):
        g = DiGraph()
        algo = GraphAlgo(g)
        algo.load_from_json("../data/A5")
        start = time.time()
        algo.shortest_path(0, 47)
        end = time.time()
        print(end - start)

    def test_time_dijkstra_networkx(self):
        pass


if __name__ == '__main__':
    unittest.main()

    # Shortest Path:
    #     python time: 0.0010039806365966797
    #     java time:   0.0022536
    #     networkX time:

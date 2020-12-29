import unittest
import random

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):

    def test_nodesize(self):
        g = create_graph_random()
        self.assertEqual(g.NumberOfNodes, 10)
        self.assertEqual(True, True)

    def test_edgeSize(self):
        g = create_graph(10, 20)
        g.add_edge(0, 1, 20)
        self.assertEqual(g.NumberOfEdges, 21)
        print("Okay21")
        if g.remove_edge(0, 1):
            self.assertEqual(g.NumberOfEdges, 20)
            print("Okay20")

        g.add_node(100)
        g.add_node(101)
        g.add_node(102)
        g.add_node(103)
        g.add_node(104)

        g.add_edge(100, 101, 10)
        g.add_edge(100, 102, 10)
        g.add_edge(100, 103, 10)
        g.add_edge(100, 104, 10)

        g.remove_node(100)
        self.assertEqual(g.NumberOfNodes, 14)
        self.assertEqual(g.NumberOfEdges, 20)


    def test_algo_load(self):
        algo = GraphAlgo()
        print(algo.load_from_json("../data/A5"))
        graph:DiGraph = algo.graph
        print(graph.NumberOfNodes)
        print(graph.NumberOfEdges)
    def test_algo_save(self):
        algo = GraphAlgo()
        algo.graph = create_graph_random()
        algo.save_to_json("Data.json")

def create_graph_random():
    g = DiGraph()
    for i in range(10):
        g.add_node(i)
    for i in range(20):
        u = random.randint(0, 9)
        v = random.randint(0, 9)
        w = random.randint(0, 100)
        g.add_edge(u, v, w)
    return g


def create_graph(nodeSize, edgeSize):
    g = DiGraph()
    for i in range(nodeSize):
        g.add_node(i)
    while g.NumberOfEdges != edgeSize:
        u = random.randint(0, nodeSize)
        v = random.randint(0, nodeSize)
        w = random.randint(0, 100)
        g.add_edge(u, v, w)
    return g


if __name__ == '__main__':
    unittest.main()

import collections
import unittest
import random
from src.data import node_data
import timeit
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from heapq import heapify, heappush, heappop


class MyTestCase(unittest.TestCase):

    def test_nodesize(self):
        g = create_graph_random()
        self.assertEqual(g.NumberOfNodes, 10)
        self.assertEqual(True, True)

    def test_edgeSize(self):
        g = create_graph(10, 20)
        g.add_edge(0, 1, 20)
        self.assertEqual(g.NumberOfEdges, 21)

        if g.remove_edge(0, 1):
            self.assertEqual(g.NumberOfEdges, 20)

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
        algo.load_from_json("../data/A1_BrokenA")
        graph: DiGraph = algo.graph
        self.assertEqual(graph.NumberOfNodes, 17)
        self.assertEqual(graph.NumberOfEdges, 19)

    def test_algo_save(self):
        algo = GraphAlgo()
        algo.graph = create_graph_random()
        algo.save_to_json("Data.json")

    def test_big_dfs(self):
        # Checking if there is an exception at some scenario
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        random.seed(55555)
        for i in range(1000):
            b = random.randint(0, 47)
            c = random.randint(0, 47)
            algo.graph.remove_edge(b, c)
            algo.graph.remove_edge(c, b)
        for i in algo.graph.nodes.keys():
            algo.connected_component(i)

    def test_big_dijkstra(self):
        # Checking if there is an exception at some scenario
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        for i in algo.graph.nodes.keys():
            for j in algo.graph.nodes.keys():
                x = algo.shortest_path(i, j)

    def test_empty_list(self):
        g = DiGraph()
        g.add_node(1)
        self.assertEqual(g.all_in_edges_of_node(1), {})

    def test_dfs(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/G_1000_8000_0.json")
        graph: DiGraph = algo.graph
        print(algo.connected_components())
        print(algo.connected_component(11))
        # self.assertEqual(len(algo.connected_component(0)), 4)
        # self.assertEqual(len(algo.connected_components()), 10)

    def test_connected_componenT(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/G_30000_240000_0.json")
        u = random.randint(0, 30000)
        list = algo.connected_components()
        wantedlist = []
        for i in list:
            if u in i:
                wantedlist = i
                break
        listA = algo.connected_component(u)
        self.assertEqual(collections.Counter(listA),collections.Counter(wantedlist))

    def test_shortest_path(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        algo.shortest_path(0, 47)

    def test_plot_on_big_random_graph(self):
        g = create_graph_random()
        algo = GraphAlgo(g)

        algo.load_from_json("../data/G_10_80_0.json")
        algo.plot_graph()

    def test_check_PQ(self):
        g = DiGraph()
        node1 = node_data(5)
        node2 = node_data(50)
        node1.tag = 5
        node2.tag = 50
        node3 = node_data(25)
        node3.tag = 25
        node4 = node_data(25)
        node4.tag = 25
        pq = []
        heapify(pq)
        heappush(pq, node3)
        heappush(pq, node2)
        heappush(pq, node1)
        heappush(pq, node4)
        self.assertEqual(heappop(pq).key, 5)
        self.assertEqual(heappop(pq).key, 25)
        self.assertEqual(heappop(pq).key, 25)


def create_graph_random():
    g = DiGraph()
    for i in range(10):
        g.add_node(i)
    for i in range(10):
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

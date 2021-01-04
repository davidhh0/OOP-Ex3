import unittest
import random
from src.data import node_data
import timeit
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):
    def test_priority_tags(self):
        # Priority Queue will be : out = min(graph.nodes , key = get_tag)
        g = DiGraph()
        for i in range(10):
            g.add_node(i)
            g.nodes[i].tag = random.randint(1, 100)
        PQ = []
        for node in g.nodes.values():
            PQ.append(node)
        while len(PQ) > 0:
            index = PQ.index(min(list(PQ), key=node_data.get_tag))
            node: node_data = PQ.pop(index)
            print(node.tag)

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
        print(algo.load_from_json("Data.json"))
        graph: DiGraph = algo.graph
        print(graph.NumberOfNodes)
        print(graph.NumberOfEdges)

    def test_algo_save(self):
        algo = GraphAlgo()
        algo.graph = create_graph_random()
        algo.save_to_json("Data.json")

    def test_big_dfs(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        random.seed(55555)
        for i in range(1000):
            b = random.randint(0, 47)
            c = random.randint(0, 47)
            algo.graph.remove_edge(b, c)
            algo.graph.remove_edge(c, b)
        for i in algo.graph.nodes.keys():
            print(algo.connected_component(i))

    def test_big_dijkstra(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        print(list(algo.graph.nodes.keys()))
        for i in algo.graph.nodes.keys():
            for j in algo.graph.nodes.keys():
                x = algo.shortest_path(i, j)

    def test_empty_list(self):
        g = DiGraph()
        g.add_node(1)
        print(g.all_in_edges_of_node(1))

    def test_dfs(self):
        algo = GraphAlgo()
        print(algo.load_from_json("../data/A5"))
        graph: DiGraph = algo.graph
        print(graph.NumberOfNodes)
        print(graph.NumberOfEdges)
        #   print(algo.connected_component(0))
        self.assertEqual(len(algo.connected_component(0)), 48)
        self.assertEqual(len(algo.connected_components()), 1)

    def test_shortest_path(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        print(algo.shortest_path(7, 7))

    def test_plot_on_big_random_graph(self):
        g = create_graph_random()
        algo = GraphAlgo(g)
        algo.plot_graph()


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

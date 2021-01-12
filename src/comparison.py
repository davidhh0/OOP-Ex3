import json
import unittest
import random
import networkx as nx
from timeit import default_timer as timer
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCaseForComparison(unittest.TestCase):
    """
        This class computes the time elapsed for DiGraph algorithms and NetworkX for:
        shortest path
        connected components
        connected component
    """

    shortestPathSumDiGraph = 0
    shortestPathSumNetworX = 0

    connectedComponentsDiGraph = 0
    connectedComponentsNetworkX = 0

    connectedComponenTDiGraph = 0
    connectedComponenTNetworkX = 0

    def test_return_graph_my(self):
        self.shortestPathSumDiGraph = 0
        list = ["G_10_80_0.json", "G_100_800_0.json", "G_1000_8000_0.json", "G_10000_80000_0.json"
            , "G_20000_160000_0.json", "G_30000_240000_0.json"]
        for i in list:
            g = GraphAlgo()
            g.load_from_json("../data/" + i)
            time_test(g.graph)

    def test_time_networkx_for_all(self):
        self.shortestPathSumNetworkX = 0
        list = ["G_10_80_0.json", "G_100_800_0.json", "G_1000_8000_0.json", "G_10000_80000_0.json"
            , "G_20000_160000_0.json", "G_30000_240000_0.json"]
        for i in list:
            g = return_graph_from_json_networkx(i)
            time_test_networkx(g)
            if i == "G_30000_240000_0.json":
                print("DiGraph: Average time for ShortestPath:", str(MyTestCaseForComparison.shortestPathSumDiGraph / 6)
                      , "\n Average time for Connected Components: ",
                      str(MyTestCaseForComparison.connectedComponentsDiGraph / 6)
                      , "\n Average time for Connected Component: ",
                      str(MyTestCaseForComparison.connectedComponenTDiGraph / 6)

                      )
                print("NetworkX: Average time for ShortestPath:",
                      str(MyTestCaseForComparison.shortestPathSumNetworX / 6)
                      , "\n Average time for Connected Components: ",
                      str(MyTestCaseForComparison.connectedComponentsNetworkX / 6)
                      , "\n Average time for Connected Component: ",
                      str(MyTestCaseForComparison.connectedComponenTNetworkX / 6)

                      )
                print("Components networkX: ", MyTestCaseForComparison.connectedComponentsNetworkX)

    def test_separate(self):
        print("=============================================================== \n")


def return_graph_from_json_networkx(str) -> nx.DiGraph:
    with open("../data/" + str) as g:
        json_data = json.loads(g.read())
    G = nx.DiGraph()

    G.add_nodes_from(
        elem['id']
        for elem in json_data["Nodes"]
    )

    lst = [(elem['src'], elem['dest'], elem['w']) for elem in json_data['Edges']]
    G.add_weighted_edges_from(lst)

    return G


def return_ten_n_graph_my(n: int) -> DiGraph:
    g = DiGraph()
    random.seed(55555)
    for i in range(10 ** n):
        g.add_node(i)
    for i in range(10 ** (n + 1)):
        u = random.randint(0, 10 ** n)
        v = random.randint(0, 10 ** n)
        w = random.randint(0, 10000)
        g.add_edge(u, v, w)
    return g


def return_ten_n_graph_networkx(n: int) -> nx.DiGraph:
    g = nx.DiGraph()
    random.seed(55555)
    for i in range(10 ** n):
        g.add_node(i)
    for i in range(10 ** (n + 1)):
        u = random.randint(0, 10 ** n)
        v = random.randint(0, 10 ** n)
        w = random.randint(0, 10000)
        g.add_edge(u, v, weight=w)
    return g


def get_strongly_connected_with_node_networkx(g: nx.DiGraph, node: int):
    for i in nx.strongly_connected_components(g):
        if node in i:
            return i


def time_test(g: DiGraph):
    random.seed(55555)
    algo = GraphAlgo(g)
    src = random.randint(0, g.NumberOfNodes)
    dest = random.randint(0, g.NumberOfNodes)
    startShortest = timer()
    algo.shortest_path(src, dest)
    endShortest = timer()
    startConnected = timer()
    algo.connected_components()
    endConnected = timer()
    component = random.randint(0, g.NumberOfNodes)
    startComponent = timer()
    algo.connected_component(component)
    endComponent = timer()

    print("My DiGraph:", g, " ->", "\n",
          "Shortest Path:",
          (endShortest - startShortest), "\n",
          "Connected Components:",
          (endConnected - startConnected), "\n",
          "Connected Component:",
          (endComponent - startComponent), "\n")
    MyTestCaseForComparison.shortestPathSumDiGraph += (endShortest - startShortest)
    MyTestCaseForComparison.connectedComponentsDiGraph += (endConnected - startConnected)
    MyTestCaseForComparison.connectedComponenTDiGraph += (endComponent - startComponent)


def time_test_networkx(g: nx.DiGraph):
    random.seed(55555)

    src = random.randint(0, g.number_of_nodes())
    dest = random.randint(0, g.number_of_nodes())

    print("SRC : ", src, ", DEST : ", dest)
    startShortest = timer()
    nx.shortest_path(g, source=src, target=dest, method='dijkstra', weight='weight')
    endShortest = timer()
    startConnected = timer()
    (g.subgraph(c) for c in nx.strongly_connected_components(g))
    endConnected = timer()
    component = random.randint(0, g.number_of_nodes())
    startComponent = timer()
    get_strongly_connected_with_node_networkx(g, component)
    endComponent = timer()

    print("NetworkX: " + str(g.number_of_nodes()) + " nodes ->", "\n",
          "Shortest Path:",
          (endShortest - startShortest), "\n",
          "Connected Components:",
          (endConnected - startConnected), "\n",
          "Connected Component:",
          (endComponent - startComponent), "\n"
          )
    MyTestCaseForComparison.shortestPathSumNetworX += (endShortest - startShortest)
    MyTestCaseForComparison.connectedComponenTNetworkX += (endComponent - startComponent)
    MyTestCaseForComparison.connectedComponentsNetworkX += (endConnected - startConnected)


if __name__ == '__main__':
    unittest.main()

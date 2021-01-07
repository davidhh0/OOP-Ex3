import json
import sys
import unittest
import random
from src.data import node_data
import networkx as nx
from timeit import default_timer as timer
import time
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from networkx.readwrite import json_graph


class MyTestCaseForComparison(unittest.TestCase):

    def test_time_my_class(self):
        random.seed(55555)

        # 10^2 nodes and ~~ 10^3 edges:
        n = 2
        # g = return_ten_n_graph_my(n)
        algo = GraphAlgo()
        algo.load_from_json("../data/G_30000_240000_0.json")
        g = algo.graph
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
              (endComponent - startComponent)
              )

        ##################################################################################################
        n = 1
        g = return_ten_n_graph_my(n)
        algo = GraphAlgo(g)
        src = random.randint(0, 10 ** n)
        dest = random.randint(0, 10 ** n)
        startShortest = timer()
        algo.shortest_path(src, dest)
        endShortest = timer()
        startConnected = timer()
        algo.connected_components()
        endConnected = timer()
        component = random.randint(0, 10 ** n)
        startComponent = timer()
        algo.connected_component(component)
        endComponent = timer()

        print("My DiGraph:", g, " ->", "\n",
              "Shortest Path:",
              (endShortest - startShortest), "\n",
              "Connected Components:",
              (endConnected - startConnected), "\n",
              "Connected Component:",
              (endComponent - startComponent)
              )

        #########################################################################################################

        n = 1
        g = return_ten_n_graph_my(n)
        algo = GraphAlgo(g)
        src = random.randint(0, 10 ** n)
        dest = random.randint(0, 10 ** n)
        startShortest = timer()
        algo.shortest_path(src, dest)
        endShortest = timer()
        startConnected = timer()
        algo.connected_components()
        endConnected = timer()
        component = random.randint(0, 10 ** n)
        startComponent = timer()
        algo.connected_component(component)
        endComponent = timer()

        print("My DiGraph:", g, " ->", "\n",
              "Shortest Path:",
              (endShortest - startShortest), "\n",
              "Connected Components:",
              (endConnected - startConnected), "\n",
              "Connected Component:",
              (endComponent - startComponent)
              )

    def test_time_networkx(self):
        random.seed(55555)
        # 10^2 nodes and ~~ 10^3 edges:
        g = return_ten_n_graph_networkx(2)
        src = random.randint(0, 10 ** 2)
        dest = random.randint(0, 10 ** 2)
        startShortest = timer()
        nx.shortest_path(g, source=src, target=dest, method='dijkstra', weight='weight')
        endShortest = timer()
        startConnected = timer()
        (g.subgraph(c) for c in nx.strongly_connected_components(g))
        endConnected = timer()
        component = random.randint(0, 10 ** 2)
        startComponent = timer()
        get_strongly_connected_with_node_networkx(g, component)
        endComponent = timer()

        print("NetworkX: 10^2 nodes ->", "\n",
              "Shortest Path:",
              (endShortest - startShortest), "\n",
              "Connected Components:",
              (endConnected - startConnected), "\n",
              "Connected Component:",
              (endComponent - startComponent)
              )
        # =========================== 10^4 nodes and ~~ 10^5 edges
        g = return_ten_n_graph_networkx(4)
        src = random.randint(0, 10 ** 4)
        dest = random.randint(0, 10 ** 4)
        startShortest = timer()
        nx.shortest_path(g, source=src, target=dest, method='dijkstra', weight='weight')
        endShortest = timer()
        startConnected = timer()
        (g.subgraph(c) for c in nx.strongly_connected_components(g))
        endConnected = timer()
        component = random.randint(0, 10 ** 4)
        startComponent = timer()
        get_strongly_connected_with_node_networkx(g, component)
        endComponent = timer()

        print("NetworkX: 10^4 nodes ->", "\n",
              "Shortest Path:",
              (endShortest - startShortest), "\n",
              "Connected Components:",
              (endConnected - startConnected), "\n",
              "Connected Component:",
              (endComponent - startComponent)
              )
        # ================ 10^5 nodes and ~~ 10^6 edges
        g = return_ten_n_graph_networkx(5)
        src = random.randint(0, 10 ** 5)
        dest = random.randint(0, 10 ** 5)
        startShortest = timer()
        nx.shortest_path(g, source=src, target=dest, method='dijkstra', weight='weight')
        endShortest = timer()
        startConnected = timer()
        (g.subgraph(c) for c in nx.strongly_connected_components(g))
        endConnected = timer()
        component = random.randint(0, 10 ** 5)
        startComponent = timer()
        get_strongly_connected_with_node_networkx(g, component)
        endComponent = timer()

        print("NetworkX: 10^5 nodes ->", "\n",
              "Shortest Path:",
              (endShortest - startShortest), "\n",
              "Connected Components:",
              (endConnected - startConnected), "\n",
              "Connected Component:",
              (endComponent - startComponent)
              )

    def test_time_dijkstra_my(self):
        g = DiGraph()
        algo = GraphAlgo(g)
        algo.load_from_json("../data/A5")
        start = time.time()
        algo.shortest_path(0, 47)
        end = time.time()
        print(end - start)

    def test_time_dijkstra_networkx(self):
        g = return_graph_from_json_networkx()
        start = time.time()
        print(nx.shortest_path(g, source=0, target=47, method='dijkstra', weight='weight'))
        end = time.time()
        print("NetworkX:", end - start)


def return_graph_from_json_networkx() -> nx.DiGraph:
    with open("../data/A5") as g:
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
    for i in range(10 ** (n+1)):
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


if __name__ == '__main__':
    unittest.main()

    # Shortest Path:
    #     python time: 0.0001590251922607422
    #     java time:   0.0022536
    #     networkX time: 0.0006301403045654297

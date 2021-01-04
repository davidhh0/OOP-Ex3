import json
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
        print(nx.shortest_path(g, source=0, target=47,method='dijkstra',weight='weight'))
        end = time.time()
        print("NetworkX:" , end - start)


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


if __name__ == '__main__':
    unittest.main()

    # Shortest Path:
    #     python time: 0.0001590251922607422
    #     java time:   0.0022536
    #     networkX time: 0.0006301403045654297

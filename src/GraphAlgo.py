from typing import List
import json
import queue
from src.data import node_data
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g):
        self.graph = g

    def load_from_json(self, file_name: str) -> bool:
        file_dict = None
        with open(file_name, 'r') as File:
            file_dict = json.load(File)

        if file_dict:
            self.graph = DiGraph()
            lst_nodes = list(file_dict["Nodes"])
            for node in lst_nodes:
                if "pos" in node.keys():
                    self.graph.add_node(node["id"], node["pos"])
                else:
                    self.graph.add_node(node["id"])

            lst_edges = list(file_dict["Edges"])
            for edge in lst_edges:
                self.graph.add_edge(edge["src"], edge["dest"], edge["w"])
        else:
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        answer = []
        visited = {}
        parent = {}
        PQ = []
        sofi = None

        # Priority Queue will be : out = min(graph.nodes , key = get_tag)
        g: DiGraph = self.graph
        for node in g.nodes.values():
            node.tag = float('inf')
            visited[node.key] = False
        g.nodes[id1].tag = 0
        PQ.append(g.nodes[id1])
        flag = True
        while len(PQ) > 0 and flag:
            index = PQ.index(min(list(PQ), key=node_data.get_tag))
            node: node_data = PQ.pop(index)
            if node.key == id2:
                sofi = node
                flag = False
            visited[node.key] = True
            for neig in g.edges[node.key]:
                if visited[neig] == False:
                    distance = node.tag + g.edges[node.key][neig]
                    if distance < g.nodes[neig].tag:
                        g.nodes[neig].tag = distance
                        parent[g.nodes[neig]] = node
                        PQ.append(g.nodes[neig])
        if sofi == None or sofi.key != id2:
            return None
        answer.append(g.nodes[id2])
        while True:
            if sofi.key == id1:
                break
            dad: node_data = parent[sofi]
            answer.insert(0, dad)
            sofi = parent[sofi]

        return g.nodes[id2].tag, answer

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

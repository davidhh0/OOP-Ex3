from typing import List
import json

from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self):
        self.graph = None


    def load_from_json(self, file_name: str) -> bool:
        file_dict = None
        with open(file_name,'r') as File:
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
                self.graph.add_edge(edge["src"],edge["dest"],edge["w"])
        else:
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        path = []




    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

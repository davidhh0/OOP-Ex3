from typing import List
import json

from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.data import nodeDataEncoder


class GraphAlgo(GraphAlgoInterface):

    def __init__(self):
        self.graph = None

    def load_from_json(self, file_name: str) -> bool:
        file_dict = None
        with open(file_name, 'r') as File:
            file_dict = json.load(File)

        if file_dict:
            self.graph = DiGraph()
            lst_nodes = list(file_dict["Nodes"])
            for node in lst_nodes:
                if "pos" in node.keys():
                    pos_tuple = tuple(map(float, node["pos"].split(',')))
                    self.graph.add_node(node["id"], pos_tuple)
                else:
                    self.graph.add_node(node["id"])

            lst_edges = list(file_dict["Edges"])

            for edge in lst_edges:
                self.graph.add_edge(edge["src"], edge["dest"], edge["w"])
        else:
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:

        try:

            nodes_str:dict = json.loads(nodeDataEncoder().encode(self.graph.nodes))
            nodes_lst = list(nodes_str.values())
            for node_d in nodes_lst:
                node_d["id"]=node_d["key"]
                if(node_d["pos"] == None):
                    del node_d["pos"]
                del node_d["key"]
                del node_d["tag"]

            edges_list = []
            for id in self.graph.edges.keys():
                nodes_edges_lst = list(self.graph.edges[id].keys())
                for id2 in nodes_edges_lst:
                    edges_dict = {"src": id, "dest" : id2, "w" : self.graph.edges[id][id2]}
                    edges_list.append(edges_dict)

            data = {"Nodes" : nodes_lst, "Edges":edges_list}
            with open(file_name, 'w') as File:
                File.writelines(str(data))

            return True


        except Exception as e:
            print(e.d)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        path = []

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

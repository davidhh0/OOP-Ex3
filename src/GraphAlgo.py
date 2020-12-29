from typing import List
import json
import queue
from src.data import node_data
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.data import nodeDataEncoder


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g=None):
        self.graph = g

    def load_from_json(self, file_name: str) -> bool:
        file_dict = None
        with open(file_name, 'r') as File:
            file_dict = json.loads(File.read())

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
        try:

            nodes_str: dict = json.loads(nodeDataEncoder().encode(self.graph.nodes))
            nodes_lst = list(nodes_str.values())
            for node_d in nodes_lst:
                node_d["id"] = node_d["key"]
                if (node_d["pos"] == None):
                    del node_d["pos"]
                del node_d["key"]
                del node_d["tag"]

            edges_list = []
            for id in self.graph.edges.keys():
                nodes_edges_lst = list(self.graph.edges[id].keys())
                for id2 in nodes_edges_lst:
                    edges_dict = {"src": id, "dest": id2, "w": self.graph.edges[id][id2]}
                    edges_list.append(edges_dict)

            data = {"Nodes": nodes_lst, "Edges": edges_list}
            with open(file_name, 'w') as File:
                data_str = str(data).replace("'", '"')
                File.write(data_str)

            return True


        except Exception as e:
            print(e.d)
            return False

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

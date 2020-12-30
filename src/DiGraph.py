from src.GraphInterface import GraphInterface
import src.data as data


class DiGraph(GraphInterface):

    def __init__(self):
        self.NumberOfNodes = 0
        self.NumberOfEdges = 0
        self.ModeCount = 0
        self.nodes = {}
        self.edges = {}
        self.outEdges = {}
        self.inComingEdges = {}

    def v_size(self) -> int:
        return self.NumberOfNodes

    def e_size(self) -> int:
        return self.NumberOfEdges

    def get_all_v(self) -> dict:
        return list(self.nodes.values())

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes.keys():
            return False
        node = data.node_data(node_id, pos)
        self.edges[node_id] = dict()
        self.nodes[node_id] = node
        self.NumberOfNodes += 1
        self.ModeCount += 1
        return True

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.nodes or id2 not in self.nodes:
            return False
        if id2 in self.edges[id1]:
            return False
        self.edges[id1][id2] = weight

        # ======================= Add a new edge from id1 to id2 to outEdges dict -> set================================
        if id1 not in self.outEdges.keys():
            self.outEdges[id1] = dict()
            self.outEdges[id1][id2] = weight
        else:
            self.outEdges[id1][id2] = weight
        # =============================================================================================================

        # ======================= Add a new edge from id1 to id2 to inComingEdges dict -> set==========================
        if id2 not in self.inComingEdges.keys():
            self.inComingEdges[id2] = dict()
            self.inComingEdges[id2][id1] = weight
        else:
            self.inComingEdges[id2][id1] = weight
        # =============================================================================================================

        self.NumberOfEdges += 1
        self.ModeCount += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes.keys():
            return False
        del self.nodes[node_id]
        numberOfEdges = len(self.edges[node_id].keys())
        del self.edges[node_id]
        if node_id in self.outEdges.keys():
            del self.outEdges[node_id]
        for id, dic in self.inComingEdges.items():
            if node_id in dic.keys():
                del dic[node_id]
        self.NumberOfNodes -= 1
        self.ModeCount += 1
        self.NumberOfEdges -= numberOfEdges

        # ============================== Consider deleting all edges FROM and TO node_id!!==============================
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id2 not in self.edges[node_id1] or node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False
        del self.edges[node_id1][node_id2]
        del self.outEdges[node_id1][node_id2]
        del self.inComingEdges[node_id2][node_id1]

        self.ModeCount += 1
        self.NumberOfEdges -= 1
        return True

    def get_mc(self) -> int:
        return self.ModeCount

    def all_in_edges_of_node(self, id1: int) -> dict:
        if id1 not in self.inComingEdges.keys():
            return {}
        return self.inComingEdges[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        if id1 not in self.outEdges.keys():
            return {}
        return self.outEdges[id1]

    def __repr__(self):
        return "Graph: |V|=" + str(self.NumberOfNodes) + " , |E|=" + str(self.NumberOfEdges)

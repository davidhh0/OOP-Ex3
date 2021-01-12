from src.GraphInterface import GraphInterface
import src.data as data


class DiGraph(GraphInterface):
    """
        This class represents a directed weighted graph.
        Each node has an unique key value, and edges referred as edges[source][destination] = weight
    """
    def __init__(self):
        self.NumberOfNodes = 0
        self.NumberOfEdges = 0
        self.ModeCount = 0
        self.nodes = {}
        self.edges = {}
        self.outEdges = {}
        self.inComingEdges = {}

    def v_size(self) -> int:
        """
            returns number of nodes in the graph.
        """
        return self.NumberOfNodes

    def e_size(self) -> int:
        """
            returns total number of edges in the graph.
        """
        return self.NumberOfEdges

    def get_all_v(self) -> dict:
        """
            returns all vertices in the graph as a dictionary with attributes:
            number of edges out from the vertex and number of edges in coming to the vertex.
        """
        idict = {}
        for i in self.nodes.keys():
            idict[i] = "|edges out| " + str(len(self.all_out_edges_of_node(i))) + " |edges in| " + str(
                len(self.all_in_edges_of_node(i)))
        return idict

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
            This method adds a new node to the graph with an optional position adding.
            if the key value of the node is already in the graph, the method does nothing.
        """
        if node_id in self.nodes.keys():
            return False
        node = data.node_data(node_id, pos)
        self.edges[node_id] = dict()
        self.nodes[node_id] = node
        self.NumberOfNodes += 1
        self.ModeCount += 1
        return True

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
            This method connects to nodes with a given weight.
            If at least one of the nodes key values are not in the graph or there is already an edge from id1
            to id2 , the method does nothing.
        """
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
        """
            This method deletes a node from the graph, also considering the edges from the node and in the node.
            If the node is not in the graph, the method does nothing.
        """
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
        """
            This method simply deletes an edge from id1 to id2.
            If one of the nodes are not in the graph or there isn't an edge from id1 to id2, the method does nothing.
        """
        if node_id1 not in self.edges.keys():
            return False
        if node_id2 not in self.edges[
            node_id1].keys() or node_id1 not in self.nodes.keys() or node_id2 not in self.nodes.keys():
            return False
        del self.edges[node_id1][node_id2]
        del self.outEdges[node_id1][node_id2]
        del self.inComingEdges[node_id2][node_id1]

        self.ModeCount += 1
        self.NumberOfEdges -= 1
        return True

    def get_mc(self) -> int:
        """
            returns how many changes the graph has had.
        """
        return self.ModeCount

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
            returns a dictionary of node keys that have an edge to the given id1
        """
        if id1 not in self.inComingEdges.keys():
            return {}
        return self.inComingEdges[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
            returns a dictionary of node keys that have an edge from them to the given id1
        """
        if id1 not in self.outEdges.keys():
            return {}
        return self.outEdges[id1]

    def __repr__(self):
        """
            returns a nice string for representing the graph.
        """
        return "Graph: |V|=" + str(self.NumberOfNodes) + " , |E|=" + str(self.NumberOfEdges)

    def aux_neighbor_set(self, id: int):
        """
            auxiliary function that returns neighbors of given id - meaning all the nodes connected to id
            in coming or out coming.
        """
        setofneighbors = set()
        if id in self.outEdges.keys():
            for i in self.outEdges[id].keys():
                setofneighbors.add(i)
        if id in self.inComingEdges.keys():
            for j in self.inComingEdges[id].keys():
                setofneighbors.add(j)
        return setofneighbors

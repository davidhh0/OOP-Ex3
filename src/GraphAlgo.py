import math
from typing import List
import json
import numpy as np
import matplotlib.pyplot as plt
from data import node_data
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from data import nodeDataEncoder
from DFS import dfs
import matplotlib.patheffects as pe
from heapq import heapify, heappush, heappop


class GraphAlgo(GraphAlgoInterface):

    def get_graph(self):
        return self.graph

    def __init__(self, g=None):
        self.graph: DiGraph = g
        self.dfs_colorMap = {}
        self.dfs_parent = {}
        self.dfs_start = {}
        self.dfs_finish = {}
        self.dfs_finish_transpose = {}
        self.dfs_time = 0

    def load_from_json(self, file_name: str) -> bool:

        """
        This method gets a path to json file and parse it to graph.
        Create an empty graph, and adding all the nodes from the json file.
        At last adding all edges.
        returns true if succeeded else false

        """
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

        """
            This method generate json file from graph and save it in the given path.
            For each node create a simple dictionary with key and pos, for each edge create dictionary with
            source , destination , weight and adding them to the list.
            for last save the json file to the given path.
        """
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
        """
            This method calculates the shortest path from id1 to id2 using Dijkstra's algorithm.
            The priority queue is implemented by a min heap so at any poll of the queue, the node with
            the smallest tag value will be popped.
            returns true if succeeded else false

        """
        if id1 not in self.graph.nodes.keys() or id2 not in self.graph.nodes.keys():
            return float('inf'), []
        answer = []
        visited = {}
        parent = {}
        PQ = []
        heapify(PQ)
        sofi = None

        g: DiGraph = self.graph
        for node in g.nodes.values():
            node.tag = float('inf')
            visited[node.key] = False
        g.nodes[id1].tag = 0
        heappush(PQ, g.nodes[id1])
        flag = True
        while len(PQ) > 0 and flag:
            node = heappop(PQ)
            if node.key == id2:
                sofi = node
                flag = False
            visited[node.key] = True
            for neig in g.edges[node.key]:
                if visited[neig] == False:
                    distance = node.tag + g.edges[node.key][neig]
                    if distance < g.nodes[neig].tag:
                        g.nodes[neig].tag = distance
                        parent[g.nodes[neig].key] = node
                        heappush(PQ, g.nodes[neig])
        if sofi is None or sofi.key != id2:
            return float('inf'), []
        answer.append(g.nodes[id2].key)
        while True:
            if sofi.key == id1:
                break
            dad: node_data = parent[sofi.key]
            answer.insert(0, dad.key)
            sofi = parent[sofi.key]

        return g.nodes[id2].tag, answer

    def connected_component(self, id1: int) -> list:
        """
            This method creates a new object called "dfs".
            after that calculates the connected component of specified id1 and return it's list.
            for further information step into the dfs class
        """
        if self.graph is None or id1 not in self.graph.nodes:
            return []
        run = dfs(self.graph)
        run.connected_component_for_given_node(id1)
        return run.list

    def connected_components(self) -> List[list]:
        """
            This method returns all the strongly connected components in the graph as a list of lists.
            for further information step into the dfs class
        """
        if self.graph is None:
            return []
        run = dfs(self.graph)
        run.connected_components()

        return run.list

    import math
    def distance(self, p1, p2):
        """
            returns distance between two points.
        """
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def closest(self, pt, others):
        """
        returns the minimum distance between pt to others list.
        """
        return min(others, key=lambda i: self.distance(pt, i))


    def plot_nodes(self):
        """
            This method draws the graph using matplotlib.
            In case there is a position for a node , it draws it accordingly, otherwise, it draws the node
            relatively close to it's neighbors and the other nodes in the graph.
        """
        fig, ax = plt.subplots()
        np.random.seed(555555)
        nodeIDtoCordinate = {}  # {id1: (x,y) , id2: (x,y) ...... }
        isNodeDrawn = {}  # {id1: True , id2: False...} true for a drawn node and false for a undrawn node

        for key, value in self.graph.nodes.items():
            if value.pos:
                isNodeDrawn[key] = True
                x = float(self.graph.nodes[key].pos.split(',')[0])
                y = float(self.graph.nodes[key].pos.split(',')[1])
                nodeIDtoCordinate[key] = (x, y)

            else:
                isNodeDrawn[key] = False
        closeX=float('inf')
        closeY=float('inf')
        for i in self.graph.nodes.keys():
            #  print(self.graph.aux_neighbor_set(i))
            if isNodeDrawn[i] is False:
                x, y = np.random.normal(35.1, 0.01, (1,))[0], np.random.normal(32.1, 0.01, (1,))[0]
                # x,y = np.random.randint(0,1000) , np.random.randint(0,1000)
                nodeIDtoCordinate[i] = (x, y)
                isNodeDrawn[i] = True
            for j in self.graph.aux_neighbor_set(i):
                if isNodeDrawn[j] is False:
                    closeX = nodeIDtoCordinate[i][0]
                    closeY = nodeIDtoCordinate[i][1]
                    list_pos = []
                    for k in self.graph.aux_neighbor_set(i):
                        if isNodeDrawn[k] is True and nodeIDtoCordinate[k][0] != closeX and nodeIDtoCordinate[k][
                            1] != closeY:
                            list_pos.append((nodeIDtoCordinate[k][0], nodeIDtoCordinate[k][1]))
                    if (len(list_pos) > 0):
                        closted = self.closest((closeX, closeY), list_pos)
                        deist = self.distance(closted, nodeIDtoCordinate[i])
                        # deist = self.avgDistance((closeX,closeY), list_pos)
                    else:
                        deist = 0.005
                    x, y = np.random.normal(closeX, deist, (1,))[0], np.random.normal(closeY, deist, (1,))[0]

                    if (-0.01) * deist < x - closeX < 0.01 * deist:
                        x += 0.001 * deist
                    if (-0.01) * deist < y - closeY < 0.01 * deist:
                        y += 0.001 * deist

                    nodeIDtoCordinate[j] = (x, y)
                    isNodeDrawn[j] = True
        # ============ Drawing nodes ===============
        list_pos = []
        deist = 0
        for k in self.graph.aux_neighbor_set(i):
            if closeX is  not float('inf') and closeY is not float('inf') and isNodeDrawn[k] is True and nodeIDtoCordinate[k][0] != closeX and nodeIDtoCordinate[k][1] != closeY:
                list_pos.append((nodeIDtoCordinate[k][0], nodeIDtoCordinate[k][1]))
        if (len(list_pos) > 0):
            closted = self.closest((closeX, closeY), list_pos)
            deist = self.distance(closted, nodeIDtoCordinate[i])
        for i in self.graph.nodes.keys():
            x = nodeIDtoCordinate[i][0]
            y = nodeIDtoCordinate[i][1]
            circle1 = plt.Circle((x, y), deist * 0.04, color='orange')
            ax.add_artist(circle1)
        # ============[F] Drawing nodes ===============
        # ============ Drawing arrows + edges ===============
        for i in self.graph.edges.keys():
            for j in self.graph.edges[i].keys():
                x, y = nodeIDtoCordinate[i][0], nodeIDtoCordinate[i][1]
                x2, y2 = nodeIDtoCordinate[j][0], nodeIDtoCordinate[j][1]
                headW = 0.0004
                headL = 0.0004
                r = deist * 0.04
                dxy1 = math.dist([x, y], [x2, y2]) - r
                if dxy1 < 0.002:
                    headL = headL * 0.7
                    headW = headW * 0.7

                r = deist * 0.04 + headL + 0.00001

                dxy = math.dist([x, y], [x2, y2]) - r
                if (r + dxy) == 0:
                    r = 2
                    dxy = -1
                xp = (x * r + x2 * dxy) / (r + dxy)
                yp = (y * r + y2 * dxy) / (r + dxy)

                dx = xp - x
                dy = yp - y

                ax.arrow(x, y, dx, dy, in_layout=False, head_width=headW, alpha=0.85, head_length=headL, width=0.00001,
                         fc='black',
                         ec='black')
        # ============[F] Drawing arrows + edges ===============

        # ============ Drawing labels for each node ============
        for i in self.graph.nodes.keys():
            x = nodeIDtoCordinate[i][0]
            y = nodeIDtoCordinate[i][1]
            # plt.annotate(str(i), (x+0.0001, y+0.0001), fontsize=10,weight='bold')
            plt.text(x + 0.0001, y + 0.0001, str(i), color='orange', fontsize=10,
                     path_effects=[pe.withStroke(linewidth=1, foreground="black")]
                     )
        # ============[F] Drawing labels for each node ============
        fig.text(0.95, 0.89, 'David & Yuval',
                 fontsize=30, color='black',
                 ha='right', va='bottom', alpha=0.3)
        plt.show()

    def plot_graph(self) -> None:
        """
            plots the graph using matplotlib.
            for further information, see self.plot_nodes.
        """
        self.plot_nodes()

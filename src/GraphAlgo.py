import math
from typing import List
import json
import numpy as np
import matplotlib.pyplot as plt
from src.data import node_data
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.data import nodeDataEncoder
from src.DFS import dfs
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
        if id1 not in self.graph.nodes.keys() or id2 not in self.graph.nodes.keys():
            return float('inf'), []
        answer = []
        visited = {}
        parent = {}
        PQ = []
        heapify(PQ)
        sofi = None

        # Priority Queue will be : out = min(graph.nodes , key = get_tag)
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
                        heappush(PQ,g.nodes[neig])
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
        if self.graph is None or id1 not in self.graph.nodes.keys():
            return []
        run = dfs(self.graph)
        run.connected_components()
        for i in run.list:
            if id1 in i:
                return i

    def connected_components(self) -> List[list]:
        if self.graph is None:
            return []
        run = dfs(self.graph)
        run.connected_components()

        return run.list

    def plot_nodes_with_pos(self):
        nodeIDtoCordinate = {}
        fig, ax = plt.subplots()
        for i in self.graph.nodes.keys():
            x = float(self.graph.nodes[i].pos.split(',')[0])
            y = float(self.graph.nodes[i].pos.split(',')[1])
            nodeIDtoCordinate[i] = (x, y)
            ax.plot(x, y, '-o', ms=10, lw=2, alpha=0.7, mfc='orange')
        plt.show()

    def plot_nodes_without_pos(self):
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
                    x, y = np.random.normal(closeX, 0.005, (1,))[0], np.random.normal(closeY, 0.005, (1,))[0]
                    if -0.0005 < x - closeX < 0.0005:
                        x += 0.0008
                    if -0.0005 < y - closeY < 0.0005:
                        y += 0.0008
                    nodeIDtoCordinate[j] = (x, y)
                    isNodeDrawn[j] = True
        # ============ Drawing nodes ===============
        for i in self.graph.nodes.keys():
            x = nodeIDtoCordinate[i][0]
            y = nodeIDtoCordinate[i][1]
            circle1 = plt.Circle((x, y), 0.0003, color='orange')
            ax.add_artist(circle1)
        # ============[F] Drawing nodes ===============
        # ============ Drawing arrows + edges ===============
        for i in self.graph.edges.keys():
            for j in self.graph.edges[i].keys():
                x, y = nodeIDtoCordinate[i][0], nodeIDtoCordinate[i][1]
                x2, y2 = nodeIDtoCordinate[j][0], nodeIDtoCordinate[j][1]
                headW = 0.0004
                headL = 0.0004
                r = 0.0003
                dxy1 = math.dist([x, y], [x2, y2]) - r
                if dxy1 < 0.002:
                    headL = headL * 0.7
                    headW = headW * 0.7

                r = 0.0003 + headL + 0.00001

                dxy = math.dist([x, y], [x2, y2]) - r
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
        self.plot_nodes_without_pos()

        # if list(self.graph.nodes.values())[0].pos:
        #     self.plot_nodes_with_pos()
        # else:
        #     self.plot_nodes_without_pos()

import operator
from typing import List
import json
import _collections
from src.data import node_data
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.data import nodeDataEncoder


class dfs:

    def __init__(self, g: DiGraph):
        self.graph: DiGraph = g
        self.dfs_colorMap = {}
        self.dfs_parent = {}
        self.dfs_start = {}
        self.dfs_finish = []
        self.dfs_finish_transpose = {}
        self.dfs_time = 0
        self.list = []
        self.greenCount = 0

    def connected_components(self, trans=False):
        if trans:
            self.dfs_transpose_run()
        else:
            self.dfs_run()

    def dfs_transpose_run(self):
        self.dfs_start.clear()
        self.dfs_finish_transpose.clear()
        self.dfs_parent.clear()
        # self.dfs_colorMap.clear()
        self.dfs_time = 0
        # ========== init the DFS on the graph =================:
        for i in self.graph.nodes.keys():
            if i not in self.dfs_colorMap.keys():
                self.dfs_colorMap[i] = 'white'
            elif self.dfs_colorMap[i] != 'green':
                self.dfs_colorMap[i] = 'white'

        while self.dfs_finish:
            node = self.dfs_finish.pop(0)
            u = node[0]
            if self.dfs_colorMap[u] == 'white':
                self.dfs_colorMap[u] = 'gray'
                self.dfs_visit_transpose(u)
                self.get_components()
        if self.greenCount != self.graph.NumberOfNodes:
            self.connected_components()

    def dfs_run(self):
        self.dfs_start.clear()
        self.dfs_finish.clear()
        self.dfs_parent.clear()
        # self.dfs_colorMap.clear()
        self.dfs_time = 0
        # ========== init the DFS on the graph =================:
        for i in self.graph.nodes.keys():
            if i not in self.dfs_colorMap.keys():
                self.dfs_colorMap[i] = 'white'
            elif self.dfs_colorMap[i] != 'green':
                self.dfs_colorMap[i] = 'white'

        for i in self.graph.nodes.keys():
            if self.dfs_colorMap[i] == 'white':
                self.dfs_visit(i)

        self.dfs_finish = sorted(self.dfs_finish, key=lambda tup: tup[1], reverse=True)
        self.connected_components(True)

    def dfs_visit(self, u):
        self.dfs_colorMap[u] = 'gray'
        self.dfs_time += 1
        self.dfs_start[u] = self.dfs_time
        for i in self.graph.edges[u].keys():
            if i in self.dfs_colorMap.keys():
                if self.dfs_colorMap[i] == 'white':
                    self.dfs_parent[i] = u
                    self.dfs_colorMap[i] = 'gray'
                    self.dfs_visit(i)
        self.dfs_colorMap[u] = 'black'
        self.dfs_time += 1
        self.dfs_finish.append((u, self.dfs_time))

    def dfs_visit_transpose(self, u):
        self.dfs_colorMap[u] = 'gray'
        self.dfs_time += 1
        self.dfs_start[u] = self.dfs_time
        for i in self.graph.inComingEdges[u].keys():
            if self.dfs_colorMap[i] == 'white':
                self.dfs_parent[i] = u
                self.dfs_visit_transpose(i)
        self.dfs_colorMap[u] = 'black'
        self.dfs_time += 1
        self.dfs_finish_transpose[u] = self.dfs_time

    def get_components(self):
        # Run through colorMap and for each black one add it to the list and color it green
        conList = []
        for i in self.dfs_colorMap.keys():
            if self.dfs_colorMap[i] == 'black':
                conList.append(i)
                self.dfs_colorMap[i] = 'green'
                self.greenCount += 1
        self.list.append(conList)

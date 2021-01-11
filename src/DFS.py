from src.DiGraph import DiGraph


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

    def connected_component_for_given_node(self, node: int, trans=False):
        if trans:
            self.dfs_transpose_run_given_id(node)
        else:
            self.dfs_run(node)

    def dfs_transpose_run_given_id(self, id: int):
        # Let list be the list of nodes in the dfs_start
        # We have the given ID
        # NOW we check that the ID is reachable from evey node from the list
        visited = {}
        for i in self.dfs_finish:
            temp = i[0]
            visited[temp] = False
        stack = []
        stack.insert(0, id)
        while stack:
            node = stack.pop(0)
            visited[node] = True
            for i in self.graph.all_in_edges_of_node(node).keys():
                if i in visited:
                    if visited[i] == False:
                        visited[i] = True
                        stack.insert(0, i)
        for i in visited.keys():
            if visited[i] == True:
                self.list.append(i)

    def dfs_transpose_run(self, id: int = None):
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
        # ======================================================
        while self.dfs_finish:
            node = self.dfs_finish.pop(0)
            u = node[0]
            if self.dfs_colorMap[u] == 'white':
                self.dfs_colorMap[u] = 'gray'
                self.dfs_visit_transpose_iterative(u)
                self.get_components()
        if self.greenCount != self.graph.NumberOfNodes:
            self.connected_components()

    def dfs_run(self, node: int = None):
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
        if node == None:
            for i in self.graph.nodes.keys():
                if self.dfs_colorMap[i] == 'white':
                    # self.dfs_visit(i)
                    self.dfs_visit_iterative(i)
        else:  # node is None
            self.dfs_visit_iterative(node)

        self.dfs_finish = sorted(self.dfs_finish, key=lambda tup: tup[1], reverse=True)
        if node == None:
            self.connected_components(True)
        else:
            self.connected_component_for_given_node(node, True)

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

    def dfs_visit_iterative(self, u):
        lst = []
        node_tup = [u, -1]
        lst.append(node_tup)

        while (len(lst) > 0):
            node_t = lst[0]
            node_t[1] += 1
            if (self.dfs_colorMap[node_t[0]] != 'gray'):
                self.dfs_time += 1
                self.dfs_start[node_t[0]] = self.dfs_time
            self.dfs_colorMap[node_t[0]] = 'gray'

            lst_keys = list(self.graph.all_out_edges_of_node(node_t[0]).keys())

            for i in range(node_t[1], len(lst_keys)):

                if self.dfs_colorMap[lst_keys[i]] == "white":
                    node_temp = [lst_keys[i], -1]
                    lst.insert(0, node_temp)
                    break

            if (lst[0][1] + 1 >= len(self.graph.all_out_edges_of_node(node_t[0]).keys())):
                self.dfs_colorMap[node_t[0]] = 'black'
                self.dfs_time += 1
                self.dfs_finish.append((node_t[0], self.dfs_time))
                lst.pop(0)

    def dfs_visit_transpose(self, u):
        self.dfs_colorMap[u] = 'gray'
        self.dfs_time += 1
        self.dfs_start[u] = self.dfs_time
        value = self.graph.inComingEdges.get(u)
        if value is not None:
            for i in self.graph.inComingEdges[u].keys():
                if self.dfs_colorMap[i] == 'white':
                    self.dfs_parent[i] = u
                    self.dfs_visit_transpose(i)
        self.dfs_colorMap[u] = 'black'
        self.dfs_time += 1
        self.dfs_finish_transpose[u] = self.dfs_time

    def dfs_visit_transpose_iterative(self, u):
        lst = []
        node_tup = [u, -1]
        lst.append(node_tup)

        while (len(lst) > 0):
            node_t = lst[0]
            node_t[1] += 1
            if (self.dfs_colorMap[node_t[0]] != 'gray'):
                self.dfs_time += 1
                self.dfs_start[node_t[0]] = self.dfs_time
            self.dfs_colorMap[node_t[0]] = 'gray'

            lst_keys = list(self.graph.all_in_edges_of_node(node_t[0]).keys())

            for i in range(node_t[1], len(lst_keys)):

                if self.dfs_colorMap[lst_keys[i]] == "white":
                    node_temp = [lst_keys[i], -1]
                    lst.insert(0, node_temp)
                    break

            if (lst[0][1] + 1 >= len(self.graph.all_in_edges_of_node(node_t[0]).keys())):
                self.dfs_colorMap[node_t[0]] = 'black'
                self.dfs_time += 1
                self.dfs_finish.append((node_t[0], self.dfs_time))
                lst.pop(0)

    def get_components(self):
        # Run through colorMap and for each black one add it to the list and color it green
        conList = []
        for i in self.dfs_colorMap.keys():
            if self.dfs_colorMap[i] == 'black':
                conList.append(i)
                self.dfs_colorMap[i] = 'green'
                self.greenCount += 1
        self.list.append(conList)

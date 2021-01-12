from src.DiGraph import DiGraph


class dfs:
    """
        This class implements Depth-first Search for a directed weighted graph.
    """
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
        """
            This function is the base for determining the connected components
            The first time it runs DFS on out edges and the second time it runs DFS on in coming edges.
        """
        if trans:
            self.dfs_transpose_run()
        else:
            self.dfs_run()

    def connected_component_for_given_node(self, node: int, trans=False):
        """
            This function is the base for determining the connected component
            The first time it runs DFS on out edges and the second time it runs DFS on in coming edges.
        """
        if trans:
            self.dfs_transpose_run_given_id(node)
        else:
            self.dfs_run(node)

    def dfs_transpose_run_given_id(self, id: int):
        """
            This method run BFS on the potential nodes that discovered during the first DFS
            potential node: all the nodes that have a path from the given id to them.
        """
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
        """
            This method runs an iterative DFS transpose as long as the finish time dictionary data structure
            is not empty.
            Meaning that we run the transpose DFS (all in coming edges)
        """
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
        """
            This method runs DFS on every node and paints the visited nodes as "black" and the unvisited
            ones remain "white".
        """
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


    def dfs_visit_iterative(self, u):
        """

        """
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
        """
            Adding to the main list the list of the "black" nodes.
        """
        # Run through colorMap and for each black one add it to the list and color it green
        conList = []
        for i in self.dfs_colorMap.keys():
            if self.dfs_colorMap[i] == 'black':
                conList.append(i)
                self.dfs_colorMap[i] = 'green'
                self.greenCount += 1
        self.list.append(conList)

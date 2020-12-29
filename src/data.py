""" this class represents a node in a graph """


class node_data:

    def __init__(self, key, pos: tuple = None):
        self.key = key
        self.tag = 0
        self.pos = pos


class edge_data:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

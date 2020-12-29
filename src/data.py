""" this class represents a node in a graph """
import json
from json import JSONEncoder


class node_data:

    def __init__(self, key, pos: tuple = None):
        self.key = key
        self.tag = 0
        self.pos = pos

    def get_tag(self):
        return self.tag

    def __repr__(self):
        if self.pos:
            return str({"pos":",".join(self.pos), "id":self.key})
        return str({"id":self.key})

class nodeDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class edge_data:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

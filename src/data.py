""" this class represents a node in a graph """
import json
from filecmp import cmp
from json import JSONEncoder


class node_data:
    """
        This class represents a node in a directed weighted graph.
        each node is defined by an unique integer key.
    """
    def __init__(self, key, pos: tuple = None):
        self.key = key
        self.tag = 0
        self.pos = pos

    def get_tag(self):
        """
            Returns the tag value for this node.
            helpful for algorithms and marking a node.
        """
        return self.tag

    def __repr__(self):
        """
            Returns a string represented the node.
        """
        if self.pos:
            return str({"pos": self.pos, "id": self.key})
        return str({"id": self.key})

    def __lt__(self, other):
        return not (self.tag > other.tag)

    def __gt__(self, other):
        return (self.tag > other.tag)

    def __eq__(self, other):
        return self.tag == other.tag


class nodeDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__



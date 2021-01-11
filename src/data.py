""" this class represents a node in a graph """
import json
from filecmp import cmp
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



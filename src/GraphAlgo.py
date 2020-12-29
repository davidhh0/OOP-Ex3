from typing import List
import json

from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self):
        self.graph = None


    def load_from_json(self, file_name: str) -> bool:
        file_dict = None
        with open(file_name,'r') as File:
            file_dict = json.load(File)

        if file_dict:
            self.graph = DiGraph()


    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        path = []




    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

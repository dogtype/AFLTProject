from typing import Set

from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge

class Hypergraph:

    def __init__(self) -> None:
        self.V = set()
        self.E = set()

    def add_edge(self, edge) -> None:
        if edge.label in {e.label for e in self.E}:
            raise RuntimeError("label already present in the graph")

        self.E.add(edge)

    def add_vertex(self, vertex) -> None:
        if vertex.label in {v.label for v in self.V}:
            raise RuntimeError("label already present in the graph")

        self.V.add(vertex)

    def cyclic(self) -> bool:
        raise NotImplementedError

    def leaves(self) -> Set[Vertex]:
        return {v for v in self.V if [v for t in [e.targets for e in self.E] for v in t].count(v) == 1}

    def visualize(self):
        import pygraphviz as pgv

        G = pgv.AGraph(strict = False, directed = False)
        G.graph_attr["label"] = "Factorgraph"
        G.node_attr["color"] = "black"
        for v in self.V:
            G.add_node(v.label,shape="circle")
        for e in self.E:
            G.add_node(e.label,shape="box", color ="red")
        for e in self.E:
            for v in e.targets:
                G.add_edge(e.label, v.label, color = "black")
        return G

    def __str__(self) -> str:
        import pygraphviz as pgv

        """ returns a dot-string representation of the graph """
        return self.visualize().string()

    def draw(self):
        import pygraphviz as pgv

        """ returns a png image of the graph """
        G = self.visualize()
        G.layout(prog="neato") # one of: neato|dot|twopi|circo|fdp|nop
        return G.draw("graph.png")

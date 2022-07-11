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

    def get_vertex(self,label) -> Vertex:
        """ returns vertex with given label """
        for v in self.V:
            if(v.label==label):
                return v

    def get_edge(self,label) -> Edge:
        """ returns edge with given label """
        for e in self.E:
            if(e.label==label):
                return e

    def cyclic(self) -> bool:
        """ returns if graph is cyclic """
        visited = set()
        stack = [] # save vertices and inEdge over which the vertex was found
        for v in self.V:
            stack.append((v,Edge(None,None))) # set inital inEdge
            while(visited != self.V and not (not stack)):
                curr, inEdge = stack.pop()
                visited.add(curr)

                for e in self.E:
                    if curr in e.targets and e != inEdge:
                        nbs = set(e.targets).difference({curr})
                        for n in nbs:
                            if n in visited:
                                return True
                            else:
                                stack.append((n,e))
        return False

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

    def __repr__(self) -> str:
        """ returns a representation of the graph """
        #print(self.V)
        #print(self.E)
        #print("V"+str(hash(frozenset(self.V)))+"|E"+str(hash(frozenset(self.E))))
        #print()
        return "V"+str(hash(frozenset(self.V)))+"|E"+str(hash(frozenset(self.E)))

    def __str__(self) -> str:
        """ returns a readable representation of the graph """
        result = "[Graph: "
        result += str(self.V)+" | "
        result+=str(self.E)
        return result + "]"

    def __eq__(self,other) -> bool:
        """ returns true if two hypergraphs have the same topology and labelling """
        if (self.V != other.V):
            return False
        if (self.E != other.E):
            return False
        return True

    def __hash__(self):
        return hash(self.__repr__())

    def draw(self):
        import pygraphviz as pgv

        """ returns a png image of the graph """
        G = self.visualize()
        G.layout(prog="neato") # one of: neato|dot|twopi|circo|fdp|nop
        return G.draw("graph.png")

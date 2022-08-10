from typing import Set

from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge

class Hypergraph:

    def __init__(self) -> None:
        self.V = set()
        self.E = set()

    def add_edge(self, edge) -> None:
        #if edge.label in {e.label for e in self.E}:
        #    raise RuntimeError("label already present in the graph")

        return self.E.add(edge)

    def add_edges(self, edgeset) -> None:
        for e in edgeset:
            self.add_edge(e)

    def add_vertex(self, vertex) -> None:
        #if vertex.label in {v.label for v in self.V}:
        #    raise RuntimeError("label already present in the graph")

        self.V.add(vertex)
    
    def add_vertices(self, vertexset) -> None:
        for v in vertexset:
            self.V.add(v)
        
    def get_vertex(self,label) -> Vertex:
        """ returns vertex with given label """
        for v in self.V:
            if(v.label==label):
                return v

    def get_edge(self,label) -> Edge:
        """ returns the edge content with given label """
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

    def __repr__(self) -> str:
        """ returns a representation of the graph """
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


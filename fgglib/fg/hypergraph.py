from typing import Set

from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge

class Hypergraph:
    '''
    A class that represents hypergraphs: graphs where every edge can connect a set of vertices
    '''

    def __init__(self) -> None:
        '''
        Creates a new Hypergraph object.

        Returns:
            Hypergraph: The newly created Hypergraph object.
        '''

        self.V = set()
        self.E = set()

    def add_edge(self, edge) -> None:
        '''
        Adds a single edge to the hypergraph

        Args:
            edge (Edge): The edge to be added
        '''

        self.E.add(edge)

    def add_edges(self, edgeset) -> None:
        '''
        Adds a set of edges to the hypergraph by calling add_edge repeatedly

        Args:
            edgeset (set): A set of edges to be added
        '''

        for e in edgeset:
            self.add_edge(e)

    def add_vertex(self, vertex) -> None:
        '''
        Adds a single vertex to the hypergraph

        Args:
            vertex (Vertex): The vertex to be added
        '''

        self.V.add(vertex)

    def add_vertices(self, vertexset) -> None:
        '''
        Adds a set of vertices to the hypergraph by calling add_vertex repeatedly

        Args:
            vertexset (set): A set of vertices to be added
        '''

        for v in vertexset:
            self.V.add(v)

    def get_vertex(self,label) -> Vertex:
        '''
        Returns a vertex with the specified label

        Args:
            label: The label requested

        Return:
            v (Vertex): A vertex from the graph with the label specified
        '''
        for v in self.V:
            if(v.label==label):
                return v

    def get_edge(self,label) -> Edge:
        '''
        Returns a edge with the specified label

        Args:
            label: The label requested

        Return:
            v (Edge): A edge from the graph with the label specified
        '''
        for e in self.E:
            if(e.label==label):
                return e

    def cyclic(self) -> bool:
        '''
        Checks if a hypergraph is cyclic

        Return:
            A boolean that states if the graph is cyclic or not
        '''
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
        '''
        Computes the leaves of a hypergraph

        Return:
            A set of vertices constituting the leave nodes of the graph
        '''
        return {v for v in self.V if [v for t in [e.targets for e in self.E] for v in t].count(v) == 1}

    def __repr__(self) -> str:
        '''
        Returns a string representation of the hypergraph

        Return:
            string: A string representation of the hypergraph consisting of vertex and edge set
        '''

        return "V"+str(hash(frozenset(self.V)))+"|E"+str(hash(frozenset(self.E)))

    def __str__(self) -> str:
        '''
        Returns a readable string representation of the hypergraph

        Return:
            result: A readable string representation of the hypergraph
            consisting of vertex and edge set
        '''

        result = "[Graph: "
        result += str(self.V)+" | "
        result+=str(self.E)
        return result + "]"

    def __eq__(self,other) -> bool:
        '''
        A predicate that checks if two hypergraphs are the same by
        comparing the vertex and edgesets

        Args:
            other (Hypergraph): the hypergraph that the current graph will be compared to

        Return:
            The result of the check
        '''
        if (self.V != other.V):
            return False
        if (self.E != other.E):
            return False
        return True

    def __hash__(self):
        '''
        A function that computes the hash value for a hypergraph object

        Return:
            The hash value computed
        '''
        return hash(self.__repr__())

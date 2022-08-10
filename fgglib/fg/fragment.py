from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge
from fgglib.fg.factorgraph import Factorgraph

class Fragment(Hypergraph):

    def __init__(self):
        super().__init__()
        self.external = []

    def add_external(self,vertex):
        if vertex.label in {v.label for v in self.external}:
            raise RuntimeError("vertex already markes")

        self.external.append(vertex)

    def nonterminals(self, NT):
        """ returns a list of nonterminals that are edge labes of the factorgraph
            and can be identified by a list of all nonterminals used """
        ntlist = []
        for e in self.E:
            if e.label in NT:
                ntlist.append(e.label)
        return ntlist

    def createEdge(self, content,label,targets): # add this as a classmethod alternatively
        e = Edge(content,label)
        for t in targets:
            e.add_target(t)
        return e
    
    def createFragment(self, vertexSet, edgeSet, external):
        frag = Fragment()
        for v in vertexSet:
            frag.add_vertex(v)
        for e in edgeSet:
            frag.add_edge(e)
        for ext in external:
            frag.add_external(ext)
        return frag

    def buildFragment(self, V, E, ext): # prohibits use of vertex label multiple times
        vertexDict = {l: Vertex(None,l) for l in V}
        vertexSet = {v for i,v in vertexDict.items()}
        edgeSet = set()
        for tup in E:
            l = tup[0]
            s = tup[1]
            vs = {vertexDict[i] for i in s}
            edgeSet.add(self.createEdge(None,l,vs))
        external = {vertexDict[e] for e in ext}
        return self.createFragment(vertexSet, edgeSet, external)
    
    def __eq__(self,other):
        return self.external == other.external and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self):
        return super().__repr__()+"|X"+str(hash(frozenset(self.external)))

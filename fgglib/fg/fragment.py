from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.vertex import Vertex
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

    def __eq__(self,other):
        return self.external == other.external and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self):
        return super().__repr__()+"|X"+str(hash(frozenset(self.external)))

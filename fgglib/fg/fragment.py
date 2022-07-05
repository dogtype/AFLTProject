from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.vertex import Vertex

class Fragment(Hypergraph):

    def __init__(self):
        super().__init__()
        self.external = set()

    def add_external(self,vertex):
        if vertex.label in {v.label for v in self.external}:
            raise RuntimeError("vertex already markes")

        self.external.add(vertex)

    def nonterminals(self, NT):
        """ returns a list of nonterminals that are edge labes of the factorgraph
            and can be identified by a list of all nonterminals used """
        ntset = set()
        for e in self.E:
            if e.label in NT:
                ntset.add(e.label)
        return ntset

    def __eq__(self,other):
        return self.external == other.external and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

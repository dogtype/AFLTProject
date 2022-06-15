from AFLTProject.fgglib.fg.hypergraph import Hypergraph

class Fragment(Hypergraph):

    def __init__(self):
        self.external = dict() # does this include nonterminals?

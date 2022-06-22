from fgglib.fg.hypergraph import Hypergraph

class Fragment(Hypergraph):

    def __init__(self):
        self.external = dict()

    def __init__(self,_V,_E,_att,_labV,_labE):
        super()

    def nonterminals(self, NT):
        """ returns a list of nonterminals that are edge labes of the factorgraph
            and can be identified by a list of all nonterminals used """
        ntlist = {}
        for e,l in self.labE:
            if l in NT:
                ntlist.add(l)
        return ntlist

from hypergraph import Hypergraph

class Fragment(Hypergraph):

    def __init__(self):
        self.external = dict()

    def __init__(self,_V,_E,_att,_labV,_labE):
        super()

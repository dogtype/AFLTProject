from hypergraph import Hypergraph

class Factorgraphs(Hypergraph):

    def __init__(self):
        super()
        self.omega = dict()
        self.phi = dict()

    def __init__(self,_V,_E,_att,_labV,_labE,_omega, _phi):
        super()
        self.omega = _omega
        self.phi = _phi

    def sum_product():
        """ returns the sum product """
        raise NotImplementedError

from fgglib.fg.hypergraph import Hypergraph

class Factorgraphs(Hypergraph):

    def __init__(self):
        super().__init__()
        self.omega = dict()
        self.phi = dict()

    def __init__(self,_V,_E,_att,_labV,_labE,_omega, _phi):
        super().__init__(_V,_E,_att,_labV,_labE)
        self.omega = _omega
        self.phi = _phi

    def sum_product():
        """ returns the sum product """
        raise NotImplementedError

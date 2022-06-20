from fgglib.fg.hypergraph import Hypergraph

class Factorgraphs(Hypergraph):

    def __init__(self, R):
        super().__init__()
        self.R = R
        self.phi = dict()

    def __init__(self,_V,_E,_att,_labV,_labE,_omega, _phi):
        super().__init__(_V,_E,_att,_labV,_labE)
        self.omega = _omega
        self.phi = _phi
        
    def add_factor(self, edge_label, function):
        phi[edge_label] = function
        
    def compute_assignment(self, arguments):
        global_function = IdentityFactorFunction(R)
        for _, local_function in self.phi.items():
            global_function *= local_function
        return global_function(arguments)
            

    def sum_product():
        """ returns the sum product, returns a dict node_label -> FactorFunction"""
        raise NotImplementedError

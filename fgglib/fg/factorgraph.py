from fgglib.fg.hypergraph import Hypergraph

class Factorgraphs(Hypergraph):

    def __init__(self, R):
        super().__init__()
        self.R = R
        self.phi = dict()

    def __init__(self,_V,_E,_att,_labV,_labE, _R _phi):
        super().__init__(_V,_E,_att,_labV,_labE)
        self.R = _R
        self.phi = _phi
        
    def add_factor(self, edge_label, function):
        phi[edge_label] = function
        
    def compute_assignment(self, arguments):
        global_function = IdentityFactorFunction(R)
        for _, local_function in self.phi.items():
            global_function *= local_function
        return global_function(arguments)
    
    def leaves(self) -> tuple[set[str], set[str]]:
        return ({self.labE[e] for e, targets in self.att.items() if len(targets) == 1}, super().leaves())

    def sum_product(self, max_iter=100):
        if self.cyclic:
            return _cyclic_sum_product(max_iter)
        else
            return _acyclic_sum_product()
        
        """ returns the sum product, returns a dict node_label -> FactorFunction"""
        raise NotImplementedError
        
    def _acyclic_sum_product(self):
        
        
    def _cyclic_sum_product(self, max_iter):
        raise NotImplementedError
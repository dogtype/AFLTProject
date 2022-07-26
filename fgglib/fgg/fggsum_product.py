import nx as nx

class FGGsum_product:
    # A helper class to compute the sum_product of a factor graph grammar

    def __init__(self, fgg):
        self.fgg = fgg
        self.variable_domain = {0.25,0.5,0.75}
        self.finite_vd = True

    def inference(self):
        """ returns the sum product of a factor graph grammar for the general case """
        if(self.finite_vd): # finite variable domain
            return self.inference_finite_variables()
        if(not fgg.recursive()): # finite graph language
            return self.inference_finite_states()
        else:
            raise Exception("Inference undecidable for infinite graph languages and infinte variable domain!") # both infinte

    def calculate_phi(self,X,xi,db):
        """ calculates the phi variable for nonterminal X """
        if("phi"+str(X)+str(xi) in db):
            return db["phi"+str(X)+str(xi)]
        result = 0
        for p in self.fgg.nProductions(X):
            for nt in p.body:
                result += self.calculate_tau(p.body,xi,db)
        db["phi"+str(X)+str(xi)]=result
        return result

    def calculate_tau(self,frag,xi,db):
        """ calculates the tau variable for fragment R """
        if("tau"+str(frag)+str(xi) in db):
            return db["phi"+str(X)+str(v)]
        result = 0
        for v in possible_variables:
            for e in frag.E:
                if(e.label in self.fgg.N): # case E_N
                    pass
                else: # case E_T
                    pass
        return result

    def inference_finite_variables(self):
        """ returns the sum product of a factor graph grammar with finite variable domain """
        if((not self.fgg.linearly_recursive()) and self.fgg.recursive()):
            raise Exception("not a linear equation system! Approximate nonlinearly")
        else:
            g = nx.Graph()
            for p in self.fgg.P:
                for nt in p.body.nonterminals(self.fgg.N):
                    g.add_edge(p.head,nt)
            comp = nx.connected_components(g)

            db = {}
            for c in comp:
                if(len(c)==1): # case (1)
                    for v in self.variable_domain: # upgrade for more variables
                        result = calculate_phi(c[0],[v],db)

            if(not self.fgg.recursive()): # we have already computed all phi values
                return calculate_phi(self.fgg.S,None,db)

            index = {}
            new_index = 0
            equations = []
            for c in comp:
                if(len(c)>1): # case (2)
                    for nt in c:
                        for p in self.fgg.nProductions(nt):
                            for v in self.variable_domain:
                                pass
            return result



    def inference_finite_states(self):
        """ returns the sum product of a factor graph grammar with finite number of states """
        raise NotImplementedError

import networkx as nx

class FGGsum_product:
    # A helper class to compute the sum_product of a factor graph grammar

    def __init__(self, fgg):
        self.fgg = fgg
        self.variable_domain = {0.25,0.5,0.75}

    def inference(self):
        """ returns the sum product of a factor graph grammar for the general case """
        if(self.fgg.finite_domain()): # finite variable domain
            return self.inference_finite_variables()
        if(not fgg.recursive()): # finite graph language
            return self.inference_finite_states()
        else:
            raise Exception("Inference undecidable for infinite graph languages and infinte variable domain!") # both infinte

    def xiX(self,X):
        """ returns a set of possible assignments to variable endpoints of an edge labelled X """
        assignments = [[]]
        for p in self.fgg.P:
            for e in p.body.E:
                if(e.label==X):
                    for t in e.targets:
                        new_assignments = []
                        for v in self.fgg.domains[t].enumerate():
                            for a in assignments:
                                ap = a.copy()
                                ap.append(v)
                                new_assignments.append(ap)
                        assignments = new_assignments
                    break
        return assignments

    def xiR(self,fragment):
        """ returns a set of possible assignments to variables of a fragment """
        assignments = [[]]
        for n in fragment.V:
            if(n not in fragment.external):
                new_assignments = []
                for v in self.fgg.domains[n].enumerate():
                    for a in assignments:
                        ap = a.copy()
                        ap.append(v)
                        new_assignments.append(ap)
                assignments = new_assignments
        return assignments

    def calculate_phi(self,X,xi,db):
        """ calculates the phi variable for nonterminal X """
        if("phi"+str(X)+str(xi) in db):
            return db["phi"+str(X)+str(xi)]
        result = 0
        for p in self.fgg.nProductions(X):
            result += self.calculate_tau(p.body,xi,db)
        db["phi"+str(X)+str(xi)]=result
        return result

    def calculate_tau(self,frag,xi,db):
        """ calculates the tau variable for fragment R """
        if("tau"+str(frag)+str(xi) in db):
            return db["phi"+str(frag)+str(xi)]
        result = 0

        for v in self.xiR(frag):
            varMap = {} # assign assigments to vertices
            index = 0
            exindex = 0
            for vtx in frag.V:
                if(vtx in frag.external):
                    varMap[vtx]=xi[exindex]
                    exindex+=1
                else:
                    varMap[vtx]=v[index]
                    index+=1

            ntproduct = 1
            tproduct = 1
            for e in frag.E: # compute changes in values
                if(e.label in self.fgg.N): # case E_N
                    asmntList = []
                    for tgt in e.targets:
                        asmntList.append(varMap[tgt])
                    ntproduct *= self.calculate_phi(e.label,asmntList,db)
                else: # case E_T
                    for tgt in e.targets:
                        tproduct *= varMap[tgt]
            result += ntproduct * tproduct

        db["phi"+str(frag)+str(xi)] = result
        return result

    def inference_finite_variables(self):
        """ returns the sum product of a factor graph grammar with finite variable domain """
        if((not self.fgg.linearly_recursive()) and self.fgg.recursive()): # Case 3
            raise Exception("not a linear equation system! Approximate nonlinearly")
        else:
            g = nx.DiGraph()
            for p in self.fgg.P:
                for nt in p.body.nonterminals(self.fgg.N):
                    g.add_edge(p.head,nt)
            comp = nx.strongly_connected_components(g)

            db = {}
            for c in comp:
                if(len(c)==1): # case (1)
                    node = c.pop()
                    for v in self.xiX(node): # upgrade for more variables
                        self.calculate_phi(node,v,db)

            print(db)

            if(not self.fgg.recursive()): # we have already computed all phi values
                return self.calculate_phi(self.fgg.S,[],db) # Case 1

            #index = {}
            #new_index = 0
            #equations = []
            #for c in comp:
            #    if(len(c)>1): # case (2)
            #        for nt in c:
            #            for p in self.fgg.nProductions(nt):
            #                for v in self.variable_domain:
            #                    pass
            #return result # Case 2



    def inference_finite_states(self):
        """ returns the sum product of a factor graph grammar with finite number of states """
        raise NotImplementedError

import networkx as nx
import numpy as np

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
                        if(t in p.body.external): # might want to introduce a nice type definition
                            continue
                        new_assignments = []
                        for v in self.fgg.domains[t].enumerate():
                            for a in assignments:
                                ap = a.copy()
                                ap.append(v)
                                new_assignments.append(ap)
                        assignments = new_assignments
                    if(assignments==[[]]):
                        continue
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
                        tproduct *= varMap[tgt] # would want to use factorfunction, but hypergraphs don't have functions!
            result += ntproduct * tproduct

        db["phi"+str(frag)+str(xi)] = result
        return result

    def inference_finite_variables(self):
        """ returns the sum product of a factor graph grammar with finite variable domain """
        g = nx.DiGraph()
        for p in self.fgg.P:
            for nt in p.body.nonterminals(self.fgg.N):
                g.add_edge(p.head,nt)
        comp = nx.strongly_connected_components(g)

        if(not self.fgg.recursive()): # Case 1
            db = {}
            for c in comp: # reverse topological order might be needed here
                if(len(c)==1): # case (1)
                    node = c.pop()
                    for v in self.xiX(node):
                        self.calculate_phi(node,v,db)

            print(db)

            return self.calculate_phi(self.fgg.S,[],db)

        elif(self.fgg.linearly_recursive()): # Case 2
            index = {}
            new_index = 0
            equations = []
            B = []


            for nt in self.fgg.N: # create phi equations
                for v in self.xiX(nt):
                    new_equation = [0]*new_index
                    if(not ("phi"+str(nt)+str(v)) in index):
                        index["phi"+str(nt)+str(v)] = new_index
                        new_index +=1
                        new_equation.append(-1)
                    else:
                        new_equation[index["phi"+str(nt)+str(v)]]=-1


                    for p in self.fgg.nProductions(nt):
                            if(("tau"+str(p.body)+str(v)) not in index):
                                index["tau"+str(p.body)+str(v)] = new_index
                                new_index +=1
                                new_equation.append(1)
                            else:
                                new_equation[index["tau"+str(p.body)+str(v)]]=1

                    equations.append(new_equation)
                    B.append(0)

                    for p in self.fgg.nProductions(nt): # create tau equations
                        new_equation = [0]*new_index
                        r = p.body
                        new_equation[index["tau"+str(r)+str(v)]]=-1
                        for var in self.xiR(r):
                            varMap = {} # assign assigments to vertices
                            curr_index = 0
                            exindex = 0
                            for vtx in r.V:
                                if(vtx in r.external):
                                    varMap[vtx]=v[exindex]
                                    exindex+=1
                                else:
                                    varMap[vtx]=var[curr_index]
                                    curr_index+=1

                            for e in r.E: # add actual variables
                                product = 1
                                if(e.label in self.fgg.N): # case E_N
                                    asmntList = []
                                    for tgt in e.targets:
                                        asmntList.append(varMap[tgt])
                                    new_equation[index["phi"+str(e.label)+str(asmntList)]]=1
                                else: # case E_T
                                    for tgt in e.targets:
                                        product *= varMap[tgt]


                            equations.append(new_equation)
                            B.append(-product)
            counter = 0
            for e in equations:
                while(len(e)<new_index):
                    e.append(0)
                print(e,"[",B[counter],"]")
                counter+=1
            print(index)
            solution = np.linalg.solve(equations,B)

            return solution

        else: # Case 3
            raise Exception("not a linear equation system! Approximate nonlinearly")




    def inference_finite_states(self):
        """ returns the sum product of a factor graph grammar with finite number of states """
        raise NotImplementedError

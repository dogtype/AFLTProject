import networkx as nx
import numpy as np
from fgglib.fg.factorfunction import FactorFunction
from fgglib.fg.factorgraph import Factorgraph
from fgglib.base.semiring import Real
from fgglib.fg.edge import FGEdge
from fgglib.fg.vertex import FGVertex
from fgglib.fg.variabledomain import VariableDomain
import pprint

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
                    if(assignments==[[]]):
                        continue
                    return assignments
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
        """ calculates the phi variable for nonterminal X directly """
        if("phi"+str(X)+str(xi) in db):
            return db["phi"+str(X)+str(xi)]
        result = 0
        for p in self.fgg.nProductions(X):
            result += self.calculate_tau(p.body,xi,db)
        db["phi"+str(X)+str(xi)]=result
        return result

    def calculate_tau(self,frag,xi,db):
        """ calculates the tau variable for fragment R directly """
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

    def create_phi_equations(self,index,new_index,equations,B,nt):
        """ creates phi equations for a nonterminal nt for the equation system"""
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

            for p in self.fgg.nProductions(nt): # create tau equations for every v
                new_index = self.create_tau_equations(index,new_index,equations,B,nt,p.body,v)

        return new_index # return the current new index. All other parameters are passed by object reference

    def create_tau_equations(self,index,new_index,equations,B,nt,r,v):
        """ creates tau equations for a production p and assignment v for the equation system """
        new_equation = [0]*new_index
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

            product = 1
            for e in r.E: # add actual variables
                if(e.label not in self.fgg.N): # case E_T
                    for tgt in e.targets:
                        product *= varMap[tgt]
            containsNT = False
            for e in r.E:
                if(e.label in self.fgg.N): # case E_N
                    containsNT = True
                    asmntList = []
                    for tgt in e.targets:
                        asmntList.append(varMap[tgt])

                    if(not ("phi"+str(e.label)+str(asmntList)) in index):
                        index["phi"+str(e.label)+str(asmntList)] = new_index
                        new_index +=1
                        new_equation.append(0) # increase length of the equation
                    new_equation[index["phi"+str(e.label)+str(asmntList)]]=product

            equations.append(new_equation)
            if(containsNT):
                B.append(0)
            else:
                B.append(-product)

        return new_index # return the current new index. All other parameters are passed by object reference

    def create_nl_phi_equations(self,index,new_index,equations,nt):
        """ creates phi equations and possibly nonlinear tau equations for the solver """
        for v in self.xiX(nt):
            new_equation = []
            if(not ("phi"+str(nt)+str(v)) in index):
                index["phi"+str(nt)+str(v)] = new_index
                new_index +=1

            new_equation.append((-1,index["phi"+str(nt)+str(v)],1))

            for p in self.fgg.nProductions(nt):
                    if(("tau"+str(p.body)+str(v)) not in index):
                        index["tau"+str(p.body)+str(v)] = new_index
                        new_index +=1

                    new_equation.append((-1,index["tau"+str(p.body)+str(v)],1))

            equations.append(self.function_from_list(new_equation))

            for p in self.fgg.nProductions(nt): # create tau equations
                new_index = self.create_nl_tau_equations(index,new_index,equations,nt,p.body,v)

        return new_index

    def create_nl_tau_equations(self,index,new_index,equations,nt,r,v):
        """ creates possibly nonlinear tau equations for the solver """
        new_equation = []
        new_equation.append((-1,index["tau"+str(r)+str(v)],1))
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

            product = 1
            for e in r.E: # add actual variables
                if(e.label not in self.fgg.N): # case E_T
                    for tgt in e.targets:
                        product *= varMap[tgt]
            occurances = {} # checks the number of times a nonterminal occurs
            for e in r.E:
                if(e.label in self.fgg.N):
                    if(e.label not in occurances):
                        occurances[e.label]=0
                    occurances[e.label]+=1

            if(len(occurances)==0):
                new_equation.append((product,0,0))

            for e in r.E:
                if(e.label in self.fgg.N and e.label in occurances): # check if the equation has been updated for e.label
                    asmntList = []
                    for tgt in e.targets:
                        asmntList.append(varMap[tgt])

                    if(not ("phi"+str(e.label)+str(asmntList)) in index):
                        index["phi"+str(e.label)+str(asmntList)] = new_index
                        new_index +=1
                    new_equation.append((product,index["phi"+str(e.label)+str(asmntList)],occurances[e.label]))
                    occurances.pop(e.label)

            equations.append(self.function_from_list(new_equation))

        return new_index

    def function_from_list(self,entries):
        """ returns a lambda function created from the list of factors in the function """
        print("equation:",entries)
        def f(x):
            result = 0
            for e in entries:
                factor, ind, exp = e
                result += factor*pow(x[ind],exp)
            return result

        return f

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

            return self.calculate_phi(self.fgg.S,[],db)

        elif(self.fgg.linearly_recursive()): # Case 2
            index = {}
            new_index = 0
            equations = []
            B = []

            for nt in self.fgg.N: # create phi equations
                new_index = self.create_phi_equations(index,new_index,equations,B,nt)

            counter = 0
            for e in equations:
                while(len(e)<new_index):
                    e.append(0)
                #print(e,"[",B[counter],"]")
                counter+=1
            solution = np.linalg.solve(equations,B)
            return solution[index["phiS[]"]]

        else: # Case 3
            from scipy.optimize import fsolve
            index = {}
            new_index = 0
            equations = [] # list of lambda functions mapping to the correct shit

            for nt in self.fgg.N: # create phi equations
                new_index = self.create_nl_phi_equations(index,new_index,equations,nt)

            def system(x):
                sol = []
                index = 0
                for xi in x:
                    sol.append(equations[index](x))
                    index+=1
                return sol

            solution = fsolve(system,[1]*new_index)
            print(index)
            print(solution)
            return round(solution[index["phiS[]"]],4) # the solver is not always precise. Return a rounded number



    def inference_finite_states(self):
        """ returns the sum product of a factor graph grammar with finite number of states """
        productions = list(self.fgg.P)
        fg = Factorgraph(productions[0].body.R)
        
        # add binary variables for all nonterminals and rules
        bin_domain = VariableDomain(False)
        bin_domain.set_content({False, True})
        nt_bin_vars = {}
        for X in self.fgg.N:
            b_var = FGVertex(X, "B_" + X, fg.R, bin_domain)
            fg.add_vertex(b_var)
            nt_bin_vars[X] = b_var
        rules_bin_vars = {}
        for i, p in enumerate(productions):
            b_var = FGVertex(p, "B_π" + str(i), fg.R, bin_domain)
            fg.add_vertex(b_var)
            rules_bin_vars[p] = b_var
        
        # add conditions to constraint to valid derivations
        start_e = FGEdge(self.fgg.S, "B_S = true", fg.R, CondStart(fg.R))
        start_e.add_target(nt_bin_vars[self.fgg.S])
        fg.add_edge(start_e)
        for X in self.fgg.N:
            if X != self.fgg.S:
                p_X_left = [p for p in productions if X == p.head]
                e = FGEdge(X, "CondOne(B_" + X + ''.join([','+rules_bin_vars[p_].label for p_ in p_X_left]) + ")", fg.R, CondOne(fg.R, 1 + len(p_X_left)))
                e.add_target(nt_bin_vars[X])
                for p in p_X_left:
                    e.add_target(rules_bin_vars[p])
                fg.add_edge(e)
                
                p_X_right = [p for p in productions if X in p.body.nonterminals(self.fgg.N)]
                e = FGEdge(X, "CondOne(B_" + X + ''.join([','+rules_bin_vars[p_].label for p_ in p_X_right]) + ")", fg.R, CondOne(fg.R, 1 + len(p_X_right)))
                e.add_target(nt_bin_vars[X])
                for p in p_X_right:
                    e.add_target(rules_bin_vars[p])
                fg.add_edge(e)
                
        # create clusters
        new_p_vars = {}
        for i, p in enumerate(productions):
            new_vars = {}
            for v in p.body.V:
                var = FGVertex(str(p), v.label + "_" + str(i), fg.R, v.domain)
                new_vars[v] = var
                e = FGEdge(str(p), "CN_" + v.label + "_" + str(i), fg.R, CondNormalize(v.domain))
                e.add_target(rules_bin_vars[p])
                e.add_target(var)
                fg.add_vertex(var)
                fg.add_edge(e)
            for e in p.body.E:
                if e.label not in self.fgg.N:
                    new_edge = FGEdge(str(p), e.label, fg.R, CondFactor(fg.R, e.function))
                    new_edge.add_target(rules_bin_vars[p])
                    for v in e.targets:
                        new_edge.add_target(new_vars[v])
                    fg.add_edge(new_edge)
            new_p_vars[p] = new_vars
            
        
                
        new_nt_vars = {}
        for X in self.fgg.N:
            for p in productions:
                if X in p.body.nonterminals(self.fgg.N):
                    X_vars = []
                    e = p.body.get_edge(X)
                    for i, t in enumerate(e.targets):
                        v = FGVertex(X, X + "_" + str(i), fg.R, t.domain)
                        X_vars.append(v)
                        new_edge = FGEdge(X, "CN_" + v.label + "_" + X, fg.R, CondNormalize(t.domain))
                        new_edge.add_target(nt_bin_vars[X])
                        new_edge.add_target(v)
                        fg.add_vertex(v)
                        fg.add_edge(new_edge)
                    new_nt_vars[X] = X_vars
                    
        # create same-variable bindings
        for X in self.fgg.N:
            for i, p in enumerate(productions):
                if X == p.head:
                    for j, v in enumerate(p.body.external):
                        new_edge = FGEdge(X, "CE_" + X + "_" + str(i) + "_" + v.label, fg.R, CondEquals(fg.R))
                        new_edge.add_target(rules_bin_vars[p])
                        new_edge.add_target(new_nt_vars[X][j])
                        new_edge.add_target(new_p_vars[p][v])
                        
                if X in p.body.nonterminals(self.fgg.N):
                    e = p.body.get_edge(X)
                    for j, t in enumerate(e.targets):
                        new_edge = FGEdge(X, "CE_" + X + "_" + str(i) + "_" + t.label, fg.R, CondEquals(fg.R))
                        new_edge.add_target(rules_bin_vars[p])
                        new_edge.add_target(new_nt_vars[X][j])
                        new_edge.add_target(new_p_vars[p][t])
                        
        return fg


class CondStart(FactorFunction):
    
    def __init__(self, R):
        super().__init__(R, 1)
        
    def compute(self, *args):
        if len(args) != arg_num:
            raise Exception("wrong number of arguments")
            
        return self.R.one if args[0] else self.R.zero
    
    
class CondOne(FactorFunction):
        
    def __init__(self, R, arg_num):
        super().__init__(R, arg_num)
        
    def compute(self, *args):
        if len(args) != self.arg_num:
            raise Exception("wrong number of arguments")
            
        if args[0]:
            return self.R.one if args[1:].count(True) == 1 else self.R.zero
        else:
            return self.R.one if args[1:].count(True) == 0 else self.R.zero
            
            
class CondEquals(FactorFunction):
    
    def __init__(self, R):
        super().__init__(R, 3)
        
    def compute(self, *args):
        if len(args) != self.arg_num:
            raise Exception("wrong number of arguments")
            
        if args[0]:
            return self.R.one if args[1] == args[2] else self.R.zero
        else:
            return self.R.one
            

class CondFactor(FactorFunction):
    
    def __init__(self, R, f):
        super().__init__(R, 1 + f.arg_num)
        self.f = f
        
    def compute(self, *args):
        if len(args) != self.arg_num:
            raise Exception("wrong number of arguments")
            
        if args[0]:
            return self.f.compute(*args[1:])
        else:
            return self.R.one
            
            
class CondNormalize(FactorFunction):
    
    def __init__(self, domain):
        super().__init__(Real, 2)
        self.weight_distr = lambda x : float(1) / float(len(domain.content))
        
    def compute(self, *args):
        if len(args) != self.arg_num:
            raise Exception("wrong number of arguments")
            
        if args[0]:
            return Real(self.weight_distr(args[1]))
        else:
            return self.R.one
from typing import Set, Tuple
from collections import defaultdict

from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.factorfunction import FactorFunction
from fgglib.fg.edge import FGEdge
from fgglib.fg.vertex import FGVertex
from fgglib.fg.variabledomain import VariableDomain
from fgglib.fg.factorfunction import MulIdentityFactorFunction

class Factorgraph(Hypergraph):

    def __init__(self, R) -> None:
        super().__init__()
        self.R = R
        
    def createVertex(self, content, label, R, domain=False):
        v = FGVertex(content, label, R, domain)
        self.add_vertex(v)
        return v
    
    def createVertices(self, contentSet, labelSet, R):
        iter = len(labelSet)
        for i in range(iter):
            if contentSet != None:
                content=contentSet[i]
            else:
                content=None
            label=labelSet[i]
            v= self.createVertex(content, label, R)
        
    def createEdge(self, content, label, targets, f, semiring):
        fgedge = FGEdge(content,label,semiring, f)
        self.add_edge(fgedge)
        for t in targets:
            fgedge.add_target(self.get_vertex(t))
            
    def set_function(self, edge, f: FactorFunction) -> None:
        for e in self.E:
            if(e.label==edge.label):
                e.function=f

    def compute_assignment(self, *args):
        result = self.R.one
        for e in self.E:
            result *= e.function.compute(*[args[v] for v in factor.targets])
        return result

    def _acyclic_sum_product(self) -> dict[FGVertex, FactorFunction]:
        states = {v:0 for v in self.V}
        states.update({e:0 for e in self.E})
        incoming_msg = {v:{e:None for e in self.E if v in e.targets} for v in self.V}
        incoming_msg.update({e:{v:None for v in e.targets} for e in self.E})
        stack = list(self.leaves() | {e for e in self.E if len(e.targets) == 1})
        while stack:
            node = stack.pop(0) # here with "node" with mean both vertices and hyperedges
            missing_neighbors = [neigh for neigh, f in incoming_msg[node].items() if f is None]
 
            if states[node] == 0 and len(missing_neighbors) == 1:
                dest = missing_neighbors.pop()
                node.set_msg(dest, incoming_msg)
                stack.append(dest)
                states[node] = 1
            elif states[node] != 2 and len(missing_neighbors) == 0:
                for dest in list(incoming_msg[node].keys()):
                    node.set_msg(dest, incoming_msg)
                    stack.append(dest)
                states[node] = 2

        return {v:v.marginal(incoming_msg) for v in self.V}

    def _cyclic_sum_product(self, max_iter) -> dict[FGVertex, FactorFunction]:
        incoming_msg = {v:{e:MulIdentityFactorFunction(self.R) for e in self.E if v in e.targets} for v in self.V}
        incoming_msg.update({e:{v:MulIdentityFactorFunction(self.R) for v in e.targets} for e in self.E})
        
        for _ in range(max_iter):
            for e in self.E:
                for t in e.targets:
                    e.set_msg(t, incoming_msg)
            for v in self.V:
                for e in self.E:
                    if v in e.targets:
                        v.set_msg(e, incoming_msg)
                        
        return {v:v.marginal(incoming_msg) for v in self.V}
                
                


    def sum_product(self, max_iter=100) -> dict[FGVertex, FactorFunction]:
        return self._cyclic_sum_product(max_iter) if self.cyclic() else self._acyclic_sum_product()
        
    def normalization_constant_(self, root=None):
        # inefficient version: generate all assignments and compute the product of the functions summing over them
        v_indexes = {v:i for i, v in enumerate(self.V)}
            
        arg_combs = []
        for v, _ in v_indexes.items():
            d = v.domain
            if len(arg_combs) == 0:
                for value in d.enumerate():
                    arg_combs.append([value])
            else:
                new_arg_combs = []
                for value in d.enumerate():
                    new_arg_combs += [a + [value] for a in arg_combs]
                arg_combs = new_arg_combs
                
        Z = self.R.zero
        for comb in arg_combs:
            cur_res = self.R.one
            for e in self.E:
                args = [comb[v_indexes[v]] for v in e.targets]
                cur_res *= e.function.compute(*args)
            Z += cur_res
        return Z
        
    def normalization_constant(self, root=None):
        # efficient version: run sum product and compute the normalization constant of a marginal
        if root is None:
            root = list(self.V)[0]
        return self.sum_product()[root].normalization_constant(root.domain)
        
    
    def createFGGraph(self, vertexSet, edgeSet, semiring):
        fg = Factorgraph(semiring)
        for v in vertexSet:
            fg.add_vertex(v)
        for e in edgeSet:
            fg.add_edge(e)
        return fg
    
    def buildGraph(V, E, semiring): # prohibits use of label multiple times
        vertexDict = {l: FGVertex(None,l,semiring) for l in V}
        vertexSet = {v for l,v in vertexDict.items()}
        edgeSet = set()
        for l,s in E.items():
            vs = [vertexDict[i] for i in s]
            edgeSet.add(self.createEdge(None, l, vs, None, semiring))
        return self.createFGGraph(vertexSet, edgeSet, semiring)
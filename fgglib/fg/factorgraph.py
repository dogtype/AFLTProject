from typing import Set, Tuple
from collections import defaultdict

from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.factorfunction import FactorFunction
from fgglib.fg.edge import FGEdge
from fgglib.fg.vertex import FGVertex

class Factorgraph(Hypergraph):

    def __init__(self, R) -> None:
        super().__init__()
        self.R = R

    def createVertex(self, content, label, R):
        v = FGVertex(content, label, R)
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
                for dest in list(incoming_msg[node].keys())[:-1]:
                    node.set_msg(dest, incoming_msg)
                    stack.append(dest)
                if states[node] == 0:
                    dest = list(incoming_msg[node].keys())[-1] #this needs to be updated
                    node.set_msg(dest, incoming_msg)
                    stack.append(dest)
                states[node] = 2

        return {v:v.marginal(incoming_msg) for v in self.V}

    def _cyclic_sum_product(self, max_iter) -> dict[FGVertex, FactorFunction]:
        raise NotImplementedError

    def sum_product(self, max_iter=100) -> dict[FGVertex, FactorFunction]:
        return self._cyclic_sum_product(max_iter) if self.cyclic() else self._acyclic_sum_product()

    def normalization_constant(self, root=None):
        if root is None:
            root = list(self.V)[0]
        return self.sum_product()[root].normalization_constant()
    
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
            vs = {vertexDict[i] for i in s}
            edgeSet.add(self.createEdge(None, l, vs, None, semiring))
        return self.createFGGraph(vertexSet, edgeSet, semiring)    

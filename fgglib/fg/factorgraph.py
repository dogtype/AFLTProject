from typing import Set, Tuple
from collections import defaultdict

from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.factorfunction import FactorFunction
from fgglib.fg.edge import FGEdge
from fgglib.fg.vertex import FGVertex
from fgglib.fg.variabledomain import VariableDomain
from fgglib.fg.factorfunction import MulIdentityFactorFunction

class Factorgraph(Hypergraph):
    '''
    A class that represents factorgraphs: hypergraphs equipped with a mapping
    to a factor function for edges and a variable domain for vertices
    '''

    def __init__(self, R) -> None:
        '''
        Creates a new Factorgraph object.

        Args:
            R(): the class of the semiring over which the factorgraph is defined

        Returns:
            Factorgraph: The newly created Factorgraph object.
        '''
        super().__init__()
        self.R = R

    def createVertex(self, content, label, R, domain=False):
        '''
        Adds a single vertex to the factorgraph

        Args:
            content: The content of the vertex to be added
            label: The label of the newly added vertex
            R: The class of the semiring over which the vertex is defined
            domain: Optional parameter for a variable domain of the new vertex
        '''
        v = FGVertex(content, label, R, domain)
        self.add_vertex(v)
        return v

    def createVertices(self, contentSet, labelSet, R, domain):
        '''
        Adds a set of vertices to the factorgraph, by calling createVertex repeatedly

        Args:
            contentSet: A set of contents for the new vertices
            labelSet: A set of labels for the new vertices
            R: The class of the semiring over which the vertices are defined
        '''
        iter = len(labelSet)
        for i in range(iter):
            if contentSet != None:
                content=contentSet[i]
            else:
                content=None
            label=labelSet[i]
            v= self.createVertex(content, label, R)

    def createEdge(self, content, label, targets, f, semiring):
        '''
        Adds a single edge to the factorgraph

        Args:
            content: The content of the edge to be added
            label: The label of the newly added edge
            targets (set): A set of target vertices of the new edge
            f (Factorfunction): The function of the edge that is to be added
            semiring (semiring): The class of the semiring over which the vertices are defined
        '''
        fgedge = FGEdge(content,label,semiring, f)
        self.add_edge(fgedge)
        for t in targets:
            fgedge.add_target(self.get_vertex(t))

    def set_function(self, edge, f: FactorFunction) -> None:
        '''
        Set a specific function for a specified edge

        Args:
            edge (Edge): The edge of which the function is to be changed
            f (Factorfunction): The function of the edge that is to be added
        '''
        for e in self.E:
            if(e.label==edge.label):
                e.function=f

    def compute_assignment(self, *args):
        '''
        Computes the value of an assignment to the variables of the factorgraph
        by multiplying individual factors

        Args:
            *args (dict): A dictionary of assignments to the variables of the graph

        Returns:
            result: The computed assignment value
        '''
        result = self.R.one
        for e in self.E:
            result *= e.function.compute(*[args[v] for v in factor.targets])
        return result

    def _acyclic_sum_product(self) -> dict[FGVertex, FactorFunction]:
        '''
        Computes the sum-product of a factorgraph for acylcic graphs

        Result:
            A dictionary mapping every vertex in the graph to its marginal
        '''
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
        '''
        Computes the sum-product of a factorgraph for cyclic graphs

        Result:
            A dictionary mapping every vertex in the graph to its marginal
        '''
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
        '''
        Computes the sum-product of a factorgraph by distinguishing between the
        cyclic and acylcic case

        Result:
            A dictionary mapping every vertex in the graph to its marginal
        '''
        return self._cyclic_sum_product(max_iter) if self.cyclic() else self._acyclic_sum_product()

    def normalization_constant_(self, root=None):
        '''
        Computes the normalizing constant of a factorgraph

        Result:
            Z (number): A single value corresponding to the normalizing constant for the graph
        '''
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
        '''
        Computes the normalizing constant of a factorgraph more efficiently

        Result:
            Z (number): A single value corresponding to the normalizing constant for the graph
        '''
        # efficient version: run sum product and compute the normalization constant of a marginal
        if root is None:
            root = list(self.V)[0]
        return self.sum_product()[root].normalization_constant(root.domain)


    def createFGGraph(self, vertexSet, edgeSet, semiring): # redundant
        '''
        Compare to the createFGGraph method in fgglib/autotesting/testenvironment
        '''
        fg = Factorgraph(semiring)
        for v in vertexSet:
            fg.add_vertex(v)
        for e in edgeSet:
            fg.add_edge(e)
        return fg

    def buildGraph(V, E, semiring): # redundant
        '''
        Compare to the buildGraph method in fgglib/autotesting/testenvironment
        '''
        vertexDict = {l: FGVertex(None,l,semiring) for l in V}
        vertexSet = {v for l,v in vertexDict.items()}
        edgeSet = set()
        for l,s in E.items():
            vs = [vertexDict[i] for i in s]
            edgeSet.add(self.createEdge(None, l, vs, None, semiring))
        return self.createFGGraph(vertexSet, edgeSet, semiring)

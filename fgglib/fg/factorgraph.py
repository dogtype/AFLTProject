from typing import Set, Tuple
from collections import defaultdict

from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.factorfunction import FactorFunction
from fgglib.fg.vertex import FGVertex

class Factorgraph(Hypergraph):

    def __init__(self, R) -> None:
        super().__init__()
        self.R = R

    def global_function(self) -> FactorFunction:
        global_function = IdentityFactorFunction(R)
        for e in self.E:
            global_function *= e.function
        return global_function

    def compute_assignment(self, arguments):
        return self.global_function().compute(arguments)

    def sum_product(self, max_iter=100) -> dict[FGVertex, FactorFunction]:
        return _cyclic_sum_product(max_iter) if self.cyclic else _acyclic_sum_product()

    def _acyclic_sum_product(self) -> dict[FGVertex, FactorFunction]:
        states = dict({v:0 for v in self.V}, **{e:0 for e in self.E})
        incoming_msg = defaultdict(lambda: defaultdict(lambda: None))
        stack = [self.leaves() | {e for e in self.E if len(e.targets) == 1}]

        while stack:
            node = stack.pop() # here with "node" with mean both vertices and hyperedges
            missing_neighbors = {neigh for neigh, f in incoming_msg[node] if f is None}
            if states[node] == 0 and len(missing_neighbors) == 1:
                dest = missing_neighbors.pop()
                node.set_msg(dest, incoming_msg)
                stack.append(dest)
                states[node] = 1
            elif states[node] != 2 and len(missing_neighbors) == 0:
                for dest in incoming_msg[node].keys()[:-1]:
                    node.set_msg(dest, incoming_msg)
                    stack.append(dest)
                if states[node] == 0:
                    node.set_msg(incoming_msg[node].keys[-1])
                    stack.append(incoming_msg[node].keys(-1))
                states[node] = 2

        return {v:v.marginal(incoming_msg) for v in self.V}

    def _cyclic_sum_product(self, max_iter) -> dict[FGVertex, FactorFunction]:
        raise NotImplementedError

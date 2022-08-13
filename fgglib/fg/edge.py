from fgglib.fg.vertex import Vertex
from fgglib.fg.factorfunction import MulIdentityFactorFunction


class Edge:
    def __init__(self, content, label) -> None:
        self.content = content
        self.label = label
        self.targets = []

    def add_target(self, vertex) -> None:
        # i believe you connect the same node multiple times with an edge
        #if vertex not in self.targets:
        self.targets.append(vertex)

    def __eq__(self,other) -> bool:
        return (self.label,self.targets)==(other.label,other.targets)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self) -> str:
        string =  "Edge "+str(self.label)+ ": "
        string += str(self.targets)
        return string


class FGEdge(Edge):
    def __init__(self, content, label, R, f) -> None:
        super().__init__(content, label)
        self.R = R
        self.function = f

    def set_msg(self, vertex, incoming_msg) -> None:
        f = self.function
        for v, msg in incoming_msg[self].items():
            if v != vertex and msg is not None and not isinstance(msg, MulIdentityFactorFunction):
                f = f.left_mul(msg, self.targets.index(v))
        incoming_msg[vertex][self] = f.marginal(self.targets.index(vertex), *[v.domain for v in self.targets])

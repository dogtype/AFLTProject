from fgglib.fg.factorfunction import IdentityFactorFunction
from fgglib.fg.vertex import Vertex


class Edge:
    def __init__(self, content, label) -> None:
        self.content = content
        self.label = label
        self.targets = set()

    def add_target(self, vertex) -> None:
        if vertex not in self.targets:
            self.targets.add(vertex)

    def __eq__(self,other) -> bool:
        return (self.label,self.targets)==(other.label,other.targets)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self) -> str:
        string =  "{Edge "+str(self.label)+ ": "
        string += str(self.targets)
        string += "}"
        return string


class FGEdge(Edge):
    def __init__(self, content, label, R, f) -> None:
        super().__init__(content, label)
        self.R = R
        self.function = f

    def set_msg(self, vertex, incoming_msg) -> None:
        f = IdentityFactorFunction(R)
        for v, msg in incoming_msg[self]:
            if v != vertex:
                f *= msg
        f = self.function * f
        incoming_msg[vertex] = f.summary(vertex.label)

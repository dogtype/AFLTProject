from fgglib.fg.factorfunction import FactorFunction, IdentityFactorFunction

class Vertex:
    def __init__(self, content, label) -> None:
        self.content = content
        self.label = label

    def __eq__(self,other) -> bool:
        return (self.label) == (other.label)

    def __hash__(self): # overwriting eq implicitely overwrites hash
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return "Vertex: "+self.label


class FGVertex(Vertex):

    def __init__(self, content, label, R, domain) -> None:
        super().__init__(content, label)
        self.R = R
        self.domain = domain

    def __eq__(self,other) -> bool:
        return (self.label, self.R) == (other.label, other.R)

    def __hash__(self): # overwriting eq implicitely overwrites hash
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return "Vertex: "+self.label+" in "+str(self.R)

    def set_msg(self, edge, incoming_msg) -> None:
        incoming_msg[edge][self] = self.marginal(incoming_msg)

    def marginal(self, incoming_msg) -> FactorFunction:
        marginal = IdentityFactorFunction(self.R)
        for _, msg in incoming_msg[self].items():
            if msg is not None:
                marginal *= msg
        return marginal

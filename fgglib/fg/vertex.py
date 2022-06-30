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

    def __init__(self, content, label, R) -> None:
        super().__init__(content, label)
        self.R = R

    def __eq__(self,other) -> bool:
        return (self.label, self.R) == (other.label, other.R)

    def __hash__(self): # overwriting eq implicitely overwrites hash
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return "Vertex: "+self.label+" in "+str(self.R)

    def set_msg(self, edge, incoming_msg) -> None:
        new_msg = IdentityFactorFunction(R)
        for _, msg in incoming_msg[self]:
            new_msg *= msg
        incoming_msg[edge] = new_msg

    def marginal(self, incoming_msg) -> FactorFunction:
        marginal = IdentityFactorFunction(R)
        for _, msg in incoming_msg[self]:
            marginal *= msg
        return marginal

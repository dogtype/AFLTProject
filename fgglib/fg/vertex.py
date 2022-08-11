from fgglib.fg.factorfunction import FactorFunction, MulIdentityFactorFunction

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
        f = MulIdentityFactorFunction(self.R)
        for e, msg in incoming_msg[self].items():
            if msg is not None and e != edge:
                f = f.left_mul(msg, 0)
        incoming_msg[edge][self] = f

    def marginal(self, incoming_msg) -> FactorFunction:
        print(self.label, "MARGINAL!!!!!")
        marginal = MulIdentityFactorFunction(self.R)
        for _, msg in incoming_msg[self].items():
            print(msg.arg_num)
            marginal = marginal.left_mul(msg, 0)
        print(marginal.arg_num)
        return marginal

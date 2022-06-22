from fgglib.fg.factorfunction import FactorFunction, IdentityFactorFunction

class Vertex:
    def __init__(self, content, label) -> None:
        self.content = content
        self.label = label
        
        
class FGVertex(Vertex):
    
    def __init__(self, content, label, R) -> None:
        super().__init__(content, label)
        self.R = R

    
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
        
from fgglib.fg.factorfunction import IdentityFactorFunction

class Edge:
    def __init__(self, content, label) -> None:
        self.content = content
        self.label = label
        self.targets = []
        
    def add_target(self, vertex) -> None:
        if vertex not in self.targets:
            self.targets.append(vertex)
        
    
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
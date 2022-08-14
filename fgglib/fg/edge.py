from fgglib.fg.vertex import Vertex
from fgglib.fg.factorfunction import MulIdentityFactorFunction


class Edge:
    '''
    A class representing an edge in a hypergraph
    '''

    def __init__(self, content, label) -> None:
        '''
        Creates a new Edge object.

        Args:
            content: The content the edge is supposed to have
            label: A label the edge should have

        Returns:
            Edge: The newly created Edge object.
        '''
        self.content = content
        self.label = label
        self.targets = []

    def add_target(self, vertex) -> None:
        '''
        Appends a new target to the list of edge targets

        Args:
            vertex (Vertex): the target to be added
        '''
        # i believe you connect the same node multiple times with an edge
        #if vertex not in self.targets:
        self.targets.append(vertex)

    def __eq__(self,other) -> bool:
        '''
        A predicate that checks if two edges are the same by comparing the labels and targets

        Args:
            other (Edge): the edge that the current edge will be compared to

        Return:
            The result of the check
        '''
        return (self.label,self.targets)==(other.label,other.targets)

    def __hash__(self):
        '''
        A function that computes the hash value for an edge object

        Return:
            The hash value computed
        '''
        return hash(self.__repr__())

    def __repr__(self) -> str:
        '''
        A function that outputs an internal representation of an edge

        Return:
            string: the string representation
        '''
        string =  "Edge "+str(self.label)+ ": "
        string += str(self.targets)
        return string


class FGEdge(Edge):
    '''
    A class representing a factor graph edge, extending the inital edge class
    '''
    def __init__(self, content, label, R, f) -> None:
        '''
        Creates a new FGEdge object.

        Args:
            content: The content the edge is supposed to have
            label: A label the edge should have
            R (): a semiring class
            f: a function which is assigned to the edge

        Returns:
            FGEdge: The newly created FGEdge object.
        '''
        super().__init__(content, label)
        self.R = R
        self.function = f

    def set_msg(self, vertex, incoming_msg) -> None:
        '''
        Compute the incoming message for this edge

        Args:
            vertex: the vertex sending a message to this edge
            incoming_msg: the multidimensional array saving the message content
        '''
        f = self.function
        for v, msg in incoming_msg[self].items():
            if v != vertex and msg is not None and not isinstance(msg, MulIdentityFactorFunction):
                f = f.left_mul(msg, self.targets.index(v))
        incoming_msg[vertex][self] = f.marginal(self.targets.index(vertex), *[v.domain for v in self.targets])

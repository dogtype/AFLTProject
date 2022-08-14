from fgglib.fg.factorfunction import FactorFunction, MulIdentityFactorFunction

class Vertex:
    '''
    A class representing a vertex in a hypergraph
    '''

    def __init__(self, content, label) -> None:
        '''
        Creates a new Vertex object.

        Args:
            content: The content the vertex is supposed to have
            label: A label the vertex should have

        Returns:
            Edge: The newly created Vertex object.
        '''
        self.content = content
        self.label = label

    def __eq__(self,other) -> bool:
        '''
        A predicate that checks if two vertices are the same by comparing the labels

        Args:
            other (Vertex): the vertex that the current vertex will be compared to

        Return:
            The result of the check
        '''
        return (self.label) == (other.label)

    def __hash__(self): # overwriting eq implicitely overwrites hash
        '''
        A function that computes the hash value for an vertex object

        Return:
            The hash value computed
        '''
        return hash(self.__repr__())

    def __repr__(self) -> str:
        '''
        A function that outputs an internal representation of a vertex

        Return:
            string: the string representation
        '''
        return "Vertex: "+self.label


class FGVertex(Vertex):
    '''
    A class representing a vertex in a factor graph, extending the inital vertex class definition
    '''

    def __init__(self, content, label, R, domain) -> None:
        '''
        Creates a new FGVertex object.

        Args:
            content: The content the vertex is supposed to have
            label: A label the edge should have
            R (): a semiring class
            f: a function which is assigned to the vertex

        Returns:
            FGVertex: The newly created FGVertex object.
        '''
        super().__init__(content, label)
        self.R = R
        self.domain = domain

    def __eq__(self,other) -> bool:
        '''
        A predicate that checks if two vertices are the same by comparing the labels and semiring

        Args:
            other (Vertex): the vertex that the current vertex will be compared to

        Return:
            The result of the check
        '''
        return (self.label, self.R) == (other.label, other.R)

    def __hash__(self): # overwriting eq implicitely overwrites hash
        '''
        See docstring for Vertex hash function
        '''
        return hash(self.__repr__())

    def __repr__(self) -> str:
        '''
        See docstring for Vertex representation
        '''
        return "Vertex: "+self.label+" in "+str(self.R)

    def set_msg(self, edge, incoming_msg) -> None:
        '''
        Compute the incoming message for this vertex

        Args:
            essge: the edge sending a message to this vertex
            incoming_msg: the multidimensional array saving message content
        '''
        f = MulIdentityFactorFunction(self.R)
        for e, msg in incoming_msg[self].items():
            if msg is not None and e != edge:
                f = f.left_mul(msg, 0)
        incoming_msg[edge][self] = f

    def marginal(self, incoming_msg) -> FactorFunction:
        '''
        Compute the marginal for this vertex

        Args:
            incoming_msg: the multidimensional array saving message content
        '''
        marginal = MulIdentityFactorFunction(self.R)
        for _, msg in incoming_msg[self].items():
            marginal = marginal.left_mul(msg, 0)
        return marginal

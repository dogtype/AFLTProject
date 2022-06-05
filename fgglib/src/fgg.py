class FGG:
    # DEFINITION
    # A factor graph grammar is a 4-Tuple <T,N,S,P> where
    # • T is a set of terminal symbols
    # • N is a set of nonterminal symbols
    # • S is a string (or label) for the starting nonterminal
    # • P is a dict, mapping nonterminal (left) to sequences of terminals and non-terminals (right)

    def __init__(self, T, N, S, P):
        self.T = T
        self.N = N
        self.S = S
        self.P = P

    def P() -> Generator:
        """ returns a generator for all production rules """
        raise NotImplementedError

    def size() -> number:
        """ returns the size of the grammar """
        raise NotImplementedError

    def recursive(self) -> bool:
        """ checks if the grammar contains recursive production rules """
        raise NotImplementedError

    def linearly_recursive(self) -> bool:
        """ checks if the grammar is linearly recursive """
        raise NotImplementedError

    def reentrant(self) -> bool:
        """ checks if the grammar is reentrant """
        raise NotImplementedError

    def conjunction(fgg : FGG) -> FGG:
        """ implements the conjunction algorithm for factor graph grammars """
        raise NotImplementedError

    def add(head, body) -> bool:
        """ helper function to add production rules """
        self.P[head] = body

    def copy() -> FGG:
        """ returns a deepcopy of the entire grammar """
        raise NotImplementedError

    def print() -> string:
        """ returns the grammar in a printable string format """
        raise NotImplementedError

    def cyclic() -> bool:
        """ returns if the grammar has cyclic productions (probably not needed) """
        raise NotImplementedError



class FGGsum_product:
    # A helper class to compute the sum_product of a factor graph grammar

    def __init__(self, fgg):
        self.fgg = fgg

    def inference()-> number:
        """ returns the sum product of a factor graph grammar for the general case """
        raise NotImplementedError

    def inference_finite_variables() -> number:
        """ returns the sum product of a factor graph grammar with finite variable domain """
        raise NotImplementedError

    def inference_finite_states() -> number:
        """ returns the sum product of a factor graph grammar with finite number of states """
        raise NotImplementedError

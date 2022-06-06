class FGG:
    # DEFINITION
    # A factor graph grammar is a 4-Tuple <T,N,S,P> where
    # • T is a set of terminal symbols
    # • N is a set of nonterminal symbols
    # • S is a string (or label) for the starting nonterminal
    # • P is a set of productions, which are in turn tuples of head and body

    def __init__(self, T, N, S, P):
        self.T = T
        self.N = N
        self.S = S
        self._P = P

    @property
    def P(self) -> Generator:
        """ returns a generator for all production rules """
		for p in self._P.items():
			yield p

    @property
    def size(self) -> number:
        """ returns the size of the grammar """
        size = 0
		for (_, body) in self.P:
			size+=len(body)+1
		return size

    def recursive(self) -> bool:
        """ checks if the grammar contains recursive production rules """
        raise NotImplementedError

    def linearly_recursive(self) -> bool:
        """ checks if the grammar is linearly recursive """
        raise NotImplementedError

    def reentrant(self) -> bool:
        """ checks if the grammar is reentrant """
        raise NotImplementedError

    def conjunction(self,fgg : FGG) -> FGG:
        """ implements the conjunction algorithm for factor graph grammars """
        raise NotImplementedError

    def add(self, head, body) -> bool:
        """ helper function to add production rules """
        if not isinstance(head, NT):
			raise InvalidProduction
		self.N.add(head)

		for elem in body:
			if isinstance(elem, NT):
				self.N.add(elem)
			elif isinstance(elem, Sym):
				self.T.add(elem)
			else:
				raise InvalidProduction

		self._P.add(Production(head, body))
        
    def copy(self) -> FGG:
        """ returns a deepcopy of the entire grammar """
		return copy.deepcopy(self)

    def print(self) -> string:
        """ returns the grammar in a printable string format """
        string = "start: " + self.S + "\n"
        for p in self.P:
            string += p.head + "--->" + p.body +"\n"
        return string

    def cyclic(self) -> bool:
        """ returns if the grammar has cyclic productions (probably not needed) """
        raise NotImplementedError



class FGGsum_product:
    # A helper class to compute the sum_product of a factor graph grammar

    def __init__(self, fgg):
        self.fgg = fgg

    def inference(self)-> number:
        """ returns the sum product of a factor graph grammar for the general case """
        raise NotImplementedError

    def inference_finite_variables(self) -> number:
        """ returns the sum product of a factor graph grammar with finite variable domain """
        raise NotImplementedError

    def inference_finite_states(self) -> number:
        """ returns the sum product of a factor graph grammar with finite number of states """
        raise NotImplementedError

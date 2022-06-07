from fgglib.fgg.exceptions import InvalidProduction
from fgglib.fgg.nonterminal import NT, S
from fgglib.fgg.production import Production

#from fgglib.graph import FGfragment


class FGG:
    # DEFINITION
    # A factor graph grammar is a 4-Tuple <T,N,S,P> where
    # • T is a set of terminal symbols (factor graph fragments)
    # • N is a set of nonterminal symbols
    # • S is a string (or label) for the starting nonterminal
    # • P is a set of productions, which are in turn tuples of head and body (fgfragment)

    def __init__(self, T, N, P): # S NT is imported
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
			size+= body.size() +1
		return size

    def recursive(self) -> bool:
        """ checks if the grammar contains recursive production rules """
        for p in P:
            nt = p.head
            if nt in p.body.N: # requires factor graph fragment to have a set of nonterminals
                return True

        return False

    def linearly_recursive(self) -> bool:
        """ checks if the grammar is linearly recursive """
        if(not self.recursive()):
            return False # grammar is nonrecursive

        for p in P:
            nt = p.head
            counter = 0
            for n in p.body.N: # requires factor graph fragment to have a set of nonterminals
                if(n==nt):
                    counter += 1
            if(counter>1):
                return False # grammar is nonlinearly recursive

        return True

    def reentrant(self) -> bool:
        """ checks if the grammar is reentrant """

        for p in P:
            size = len(p.body.N)
            if(size>1):
                return False

        return True

    def conjunction(self,fgg : FGG) -> FGG:
        """ implements the conjunction algorithm for factor graph grammars """
        raise NotImplementedError

    def add(self, head, body) -> bool:
        """ helper function to add production rules """
        if not isinstance(head, NT):
			raise InvalidProduction

		self.N.add(head)
		self.N.update(body.N)
        self.T.add(body)

		self._P.add(Production(head, body))

    def copy(self) -> FGG:
        """ returns a deepcopy of the entire grammar """
		return copy.deepcopy(self)

    def __str__(self) -> string:
        """ returns the grammar in a printable string format """
        string = "start: " + self.S + "\n"
        for p in self.P:
            string += str(p) +"\n"
        return string

    def cyclic(self) -> bool:
        """ returns if the grammar has cyclic productions (probably not needed) """
        if(self.recursive):
            return true

        curr = self.S
        searched = set()
        todo = {self.S}

        while(len(todo)>0):
            nt = todo.pop()
            if(nt in searched):
                continue
            else:
                searched.add(nt)
            for p in self.P:
                if(p.head == nt):
                    for(n in p.body.N): # requires factor graph fragment to have a set of nonterminals
                        if(n in searched):
                            return True
                        else:
                            todo.add(n)

        return False

    """
    Adapted rayuela version of cyclic
    def cyclic(self, reverse = True):
		def has_cycles(X):
			nonlocal counter
			𝜷[X] = Boolean.one
			started[X] = counter
			counter += 1
			X_productions = (p for p in self.P if p[0]==X)
			for p in X_productions:
				_, body = p
				for n in body.N: # requires factor graph fragment to have a set of nonterminals
					if n in self.T:
						continue
					elif 𝜷[n] == Boolean.one: # cycle detected
						return True
					elif has_cycles(n): # propagate cycle
						return True
			𝜷[X] = Boolean.zero
			return False

		𝜷 = Boolean.chart()
		started = {}
		counter = 0
		cyclic = has_cycles(self.S)
		if reverse:
			sort = [k for k, v in sorted(started.items(), key=lambda item: item[1])]
		else:
			sort = [k for k, v in sorted(started.items(), key=lambda item: item[1], reverse=True)]
		return cyclic, sort
    """


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

from fgglib.fgg.exceptions import *
from fgglib.fgg.nonterminal import NT, S
from fgglib.fgg.production import Production
from fgglib.fg.fragment import Fragment


class FGG:
    # DEFINITION
    # A factor graph grammar is a 4-Tuple <T,N,S,P> where
    # • T is a set of terminal symbols (factor graph fragments)
    # • N is a set of nonterminal symbols
    # • S is a string (or label) for the starting nonterminal
    # • P is a set of productions, which are in turn tuples of head and body (fgfragment)

    def __init__(self, T, N, S, P): # S NT is imported
        self.T = T
        self.N = N
        self.S = S
        self._P = P

    @property
    def P(self):
        """ returns a generator for all production rules """
        for p in self._P.items():
            yield p

    @property
    def size(self):
        """ returns the size of the grammar """
        size = 0
        for (_, body) in self.P:
            size+= body.size() +1
        return size

    def recursive(self) -> bool:
        """ checks if the grammar contains recursive production rules """
        for p in P:
            nt = p.head
            if nt in p.body.nonterminals(): # requires factor graph fragment to have a set of nonterminals
                return True

        return False

    def linearly_recursive(self) -> bool: # we might be able to use an algorithm for finding SCCs for this. Maybe split nodes (NTs) in in- and out-vertex
        """ checks if the grammar is linearly recursive """

        for p in P:
            nt = p.head

        raise NotImplementedError

    def reentrant(self) -> bool:
        """ checks if the grammar is reentrant """
        raise NotImplementedError

    def conjunction(self,fgg):
        """ implements the conjunction algorithm for factor graph grammars """
        rules = {} # set of new rules that are part of the conjoined grammar
        for p in self.P:
            for pp in fgg.P:
                if(p.conjoinable(pp)):
                    rules.add(p.conjoin(pp))
        newGrammar = FGG(self.T,self.N,self.S,rules)
        return newGrammar

    def add(self, head, body) -> bool:
        """ helper function to add production rules """
        if not isinstance(head, NT):
            raise InvalidProduction

        self.N.add(head)
        self.N.update(body.nonterminals)
        self.T.add(body)

        self._P.add(Production(head, body))

    def copy(self):
        """ returns a deepcopy of the entire grammar """
        return copy.deepcopy(self)

    def __str__(self):
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
                    for n in p.body.nonterminals: # requires factor graph fragment to have a set of nonterminals
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

    def inference(self):
        """ returns the sum product of a factor graph grammar for the general case """
        raise NotImplementedError

    def inference_finite_variables(self):
        """ returns the sum product of a factor graph grammar with finite variable domain """
        raise NotImplementedError

    def inference_finite_states(self):
        """ returns the sum product of a factor graph grammar with finite number of states """
        raise NotImplementedError

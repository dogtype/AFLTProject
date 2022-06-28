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

    def nProductions(self, n : NT):
        """ returns a set of productions starting with nonterminal n """
        result = {}
        for p in self.P:
            if(p.head!=n):
                continue
            else:
                result.add(p)
        return result

    def recursive_helper(self, visited : set, closed : set, nt : NT, curr : NT) -> bool:
        """ performs dfs """
        visited.add(nt)
        one_recursive = False
        for p in self.nProductions(curr):
            if(nt in p.body.nonterminals(self.N)):
                return True
            for n in p.body.nonterminals(self.N):
                one_recursive = one_recursive or self.recursive_helper(visited,closed,n,curr)
        closed.add(nt)
        return one_recursive

    def recursive(self) -> bool:
        """ checks if the grammar has an X-type derivation containing an X-type derivation as subtree """
        # use a simple dfs here. If we find a node that has already been visited, return true. Otherwise return false
        visited = {}
        closed = {}
        one_recursive = False
        for p in self.P:
            one_recursive = one_recursive or self.recursive_helper(visited,closed,p.head,p.head)
        return one_recursive

    def linearly_recursive_helper(self) -> bool:
        """ checks for linear recursiveness by performing a modified dfs """
        raise NotImplementedError

    def linearly_recursive(self) -> bool:
        """ checks if the grammar lacks an X-type derivation containing more than one X-type derivation as subtree """
        # use a modified dfs here. The dfs is used to return a number of found nonterminals and list of possible backtracks to check cycles
        raise NotImplementedError

    def reentrant_helper(self) -> bool:
        """ helps to check if grammar is reentrant by counting number of times every nonterminal has occured """
        raise NotImplementedError

    def duplicate_helper(self, nt: NT, duplicates : set) -> bool:
        """ returns true if the current nonterminal can produce a duplicate nt """
        if(nt in duplicates):
            return True
        else:
            one_dup = False
            for p in self.P:
                pass

    def reentrant(self) -> bool:
        """ checks if the grammar lacks a derivation containing more than one different X-type derivation as subtree """
        if (self.recursive()):
            return True
        else:
            # use another DFS here and check the number of times you find every nonterminal. A nonterminal has to be produced twice by a different one and two different derivations for this nonterminal must exist
            duplicates = {} # set of nonterminals with different derivation trees
            for p in self.P:
                pass
            for c in changeable:
                for p in self.P:
                    visited = {}
                    closed = {}
                    self.reentrant_helper(visited, closed, p, c)
            return False

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

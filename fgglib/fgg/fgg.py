from fgglib.fgg.exceptions import *
from fgglib.fgg.production import Production
from fgglib.fg.fragment import Fragment


class FGG:
    # DEFINITION
    # A factor graph grammar is a 4-Tuple <T,N,S,P> where
    # • T is a set of terminal symbols (factor graph fragments)
    # • N is a set of nonterminal symbols
    # • S is a string (or label) for the starting nonterminal
    # • P is a set of productions, which are in turn tuples of head and body (fgfragment)

    def __init__(self, T : set[Fragment], N : set, S : str, P : set[Production]): # S NT is imported
        self.T = T
        self.N = N
        self.S = S
        self._P = P

    @property
    def P(self):
        """ returns a generator for all production rules """
        for p in self._P:
            yield p


    def nProductions(self, n):
        """ returns a set of productions starting with nonterminal n """
        result = set()
        for p in self.P:
            if(p.head!=n):
                continue
            else:
                result.add(p)
        return result

    def recursion_helper(self, visited : set, closed : set, nt , curr) -> bool:
        """ performs dfs """
        visited.add(curr)
        for p in self.nProductions(curr):
            if(nt in p.body.nonterminals(self.N)):
                return True
            for n in p.body.nonterminals(self.N):
                if(n not in visited and self.recursion_helper(visited,closed,nt,n)):
                    return True
        closed.add(curr)
        return False

    def recursive(self) -> bool:
        """ checks if the grammar has an X-type derivation containing an X-type derivation as subtree """
        for p in self.P:
            if(self.recursion_helper(set(),set(),p.head,p.head)):
                return True
        return False

    def linear_recursion_helper(self, visited : set, closed : set, nt, curr) -> int:
        """ checks for linear recursiveness by performing a modified dfs """
        visited.add(curr)
        num_recursions = 0
        for p in self.nProductions(curr):
            num_prod_recursions = 0
            for n in p.body.nonterminals(self.N):
                if(n==nt):
                    num_prod_recursions+=1
            for n in p.body.nonterminals(self.N):
                if(n not in visited):
                    num_prod_recursions += self.linear_recursion_helper(visited,closed,nt,n)
            num_recursions = max(num_recursions,num_prod_recursions)
        closed.add(curr)
        return num_recursions

    def linearly_recursive(self) -> bool:
        """ checks if the grammar lacks an X-type derivation containing more than one X-type derivation as subtree """
        # use a modified dfs here. The dfs is used to return a number of found nonterminals and list of possible backtracks to check cycles
        # Does not cover all edge cases yet !!!
        num_recursions = 0
        for p in self.P:
            num_recursions = max(num_recursions,self.linear_recursion_helper(set(),set(),p.head,p.head))
        return num_recursions==1

    def duplicate(self, nt, duplicates : set) -> bool:
        """ returns true if the current nonterminal can produce a duplicate nt """
        if(nt in duplicates):
            return True
        else:
            for p in self.nProductions(nt):
                self.recursion_helper({},{},nt,p.head())

    def diffDerivTree(self) -> set:
        """ returns a set of nonterminals that have more than one different derivation tree """
        different = set()
        nts = set()
        for p in self.P:
            if(p.head in nts):
                different.add(p.head)
            nts.add(p.head)
        different_copy = set()
        while(different_copy!=different): # check if something has changed since last iteration
            different_copy = different.copy()
            for p in self.P:
                for nt in p.body.nonterminals(self.N):
                    if(nt in different):
                        different.add(p.head)
        return different


    def reentrant(self) -> bool:
        """ checks if the grammar lacks a derivation containing more than one different X-type derivation as subtree """
        if(self.recursive()):
            return True
        else:
            different = self.diffDerivTree()
            for n in self.N:
                if(n in different):
                    for np in self.N:
                        if(self.linear_recursion_helper(set(),set(),n,np)>1):
                            return True

            return False

    def conjunction(self,fgg):
        """ implements the conjunction algorithm for factor graph grammars """
        rules = set() # set of new rules that are part of the conjoined grammar
        new_T = set() # set of new terminals (fragments)  that are created by conjunction
        new_N = self.N.union(fgg.N)
        for p in self.P:
            for pp in fgg.P:
                if(p.conjoinable(pp, new_N)):
                    con = p.conjoin(pp, new_N)
                    new_T.add(con.body)
                    rules.add(con)
        newGrammar = FGG(new_T,new_N,self.S,rules)
        return newGrammar

    def add(self, head, body) -> bool:
        """ helper function to add production rules """

        self.N.add(head)
        self.N.update(body.nonterminals(self.N))
        self.T.add(body)

        self._P.add(Production(head, body))

    def copy(self):
        """ returns a deepcopy of the entire grammar """
        return copy.deepcopy(self)

    def __str__(self) -> str:
        """ returns the grammar in a printable string format """
        return self.__repr__()

    def __repr__(self) -> str():
        """ returns a representation of the grammar """
        string = "start: " + str(self.S) + "\n"
        for p in self.P:
            string += str(p) +"\n"
        return string

    def __eq__(self,other) -> bool:
        if(self.N!= other.N) or (self.S!=other.S) or (self.T!=other.T):
            return False
        for p in self.P:
            if(p not in other.P):
                return False
        for p in other.P:
            if(p not in self.P):
                return False
        return True

    def __hash__(self):
        return hash(self.__repr__())

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

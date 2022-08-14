from fgglib.fgg.production import Production
from fgglib.fg.fragment import Fragment
from fgglib.fg.factorfunction import FactorFunction


class FGG:
    '''
    A class representing a factor graph grammar. A FGG is a 4-Tuple <T,N,S,P>
    '''

    def __init__(self, T : set[Fragment], N : set, S : str, P : set[Production]): # S NT is imported
        '''
        Creates a new FGG object.

        Args:
            T (set): A set of terminals, which are factor graph fragments
            N (set): A set of nonterminal edge labels
            S: A single start symbol for the grammar
            P (set): A set of production rules with nonterminals on the left and
            factor graph fragments on the right-hand side

        Returns:
            FGG: The newly created FGG object.
        '''
        self.T = T
        self.N = N
        self.S = S
        self._P = P
        self.domains = {}

    @property
    def P(self):
        '''
        A generator for all production rules
        '''
        for p in self._P:
            yield p

    def set_function(self, edge, f: FactorFunction) -> None:
        '''
        Sets a function for a specific edge in all production rules

        Args:
            edge (Edge): The edge for which the Factorfunction is to be changed
            f (FactorFunction): The function to be assigned to edge
        '''
        for p in self.P:
            for e in p.body.E:
                if(e.label in self.N): # cannot assign functions to nonterminal edges
                    continue
                if(e==edge):
                    e.function=f

    def set_variable_domain(self,vertex_label,domain):
        '''
        Sets a variable domain for vertices (by label)

        Args:
            vetex_label: The label of the vertex for which the variable domain is set
            domain (VariableDomain): The new variabledomain for the vertices
        '''
        for p in self.P:
            for v in p.body.V:
                if(v.label==vertex_label):
                    self.domains[v] = domain

    def nProductions(self, n):
        '''
        Determines a set of productions with nonterminal n on the left-hand side

        Args:
            n: The nonterminal label to be searched

        Returns:
            result (set): The set of productions with nonterminal n on the left
        '''
        result = set()
        for p in self.P:
            if(p.head!=n):
                continue
            else:
                result.add(p)
        return result

    def recursion_helper(self, visited : set, closed : set, nt , curr) -> bool:
        '''
        A helper function to determine the recusiveness of a grammar.
        Essentially uses a modified dfs

        Args:
            visited (set): A set of nodes already visited by the traversal
            closed (set): A set of nodes closed by the traversal
            nt: The nonterminal currently searched for
            curr:  The nonterminal currently considered

        Returns:
            A boolean flag expressing if the searched nonterminal can be reached by
            productions with nonterminal curr on the left-hand side
        '''
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
        """
        Checks if the grammar has an X-type derivation containing an X-type
        derivation as subtree (definition of recursiveness by Chiang and Riley)

        Returns:
            A boolean flag expressing if the grammar is actually recursive
        """
        for p in self.P:
            if(self.recursion_helper(set(),set(),p.head,p.head)):
                return True
        return False

    def linear_recursion_helper(self, visited : set, closed : set, nt, curr) -> int:
        """
        Helper function checking for linear recursiveness by performing a modified dfs

        Args:
            visited (set): A set of nodes already visited by the traversal
            closed (set): A set of nodes closed by the traversal
            nt: The nonterminal currently searched for
            curr:  The nonterminal currently considered

        Returns:
            num_recursions (int): The number of times, a nt nonterminal can occur starting from productions
            with nonterminal curr on the left-hand side
        """
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
        '''
        Checks if the grammar lacks an X-type derivation containing more than
        one X-type derivation as subtree (definition of nonlinear recursiveness)"""

        Returns:
            A boolean flag expressing if the number of X-type derivation subtrees
            in an X-type derivation is exactly 1
        '''
        num_recursions = 0
        for p in self.P:
            num_recursions = max(num_recursions,self.linear_recursion_helper(set(),set(),p.head,p.head))
        return num_recursions==1

    def duplicate(self, nt, duplicates : set) -> bool:
        '''
        Checks if the current nonterminal can produce a duplicate nt

        Args:
            nt: Nonterminal for which the duplicate property is to be checked
            duplicates (set): A set of possible duplicates that can be found

        Returns:
            A boolean flag expressing if the specified nonterminal can produce duplicates
        '''
        if(nt in duplicates):
            return True
        else:
            for p in self.nProductions(nt):
                self.recursion_helper({},{},nt,p.head())

    def diffDerivTree(self) -> set:
        '''
        Determines a set of nonterminals that have more than one different derivation tree

        Returns:
            different (set): A set of nonterminals with the desired property
        '''
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
        '''
        Checks if the grammar lacks a X-type derivation containing more than one
        different X-type derivation as subtree (definition of nonreentrant)

        Returns:
            A boolean flag expressing if such an X-type derivation exists
        '''
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
        '''
        Implements the conjunction algorithm for factor graph grammars

        Args:
            fgg (FGG): The factor graph grammar, with which the current object is intersected

        Return:
            newGrammar (FGG): A newly generated grammar corresponding to the
            conjunction of the two original grammars
        '''
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

    def finite_domain(self) -> bool:
        for v in self.domains:
            if(self.domains[v].infinite):
                return False
        return True

    def add(self, head, body) -> bool:
        '''
        Adds a single production to the FGG while updating terminal and nonterminal sets

        Args:
            head: The nonterminal on the left-hand side of the production
            body: The FG fragement on the right-hand side of the production
        '''

        self.N.add(head)
        self.N.update(body.nonterminals(self.N))
        self.T.add(body)

        self._P.add(Production(head, body))

    def copy(self):
        '''
        Returns a deepcopy of the entire grammar

        Returns:
            The copied grammar
        '''
        return copy.deepcopy(self)

    def __str__(self) -> str:
        '''
        Returns a readable string representation of the grammar

        Returns:
            A readable string representing the grammar
        '''
        return self.__repr__()

    def __repr__(self) -> str():
        '''
        Returns a string identifying of the grammar

        Returns:
            A string identifying the grammar
        '''
        string = "start: " + str(self.S) + "\n"
        for p in self.P:
            string += str(p) +"\n"
        return string

    def __eq__(self,other) -> bool:
        '''
        A predicate that checks if two FGGs are the same by comparing the
        nonterminal and terminal sets, as well as the production rules

        Args:
            other (FGG): the FGG that the current grammar will be compared to

        Return:
            The result of the check
        '''
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
        '''
        A function that computes a hash value for a FGG object

        Return:
            The hash value computed
        '''
        return hash(self.__repr__())

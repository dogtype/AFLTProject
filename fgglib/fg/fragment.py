from fgglib.fg.hypergraph import Hypergraph
from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge
from fgglib.fg.factorgraph import Factorgraph

class Fragment(Factorgraph):
    '''
    A class that represents factorgraph fragments: factorgraphs equipped with a set
    of external nodes
    '''

    def __init__(self, R):
        '''
        Creates a new Fragment object.

        Args:
            R(): the class of the semiring over which the fragment is defined

        Returns:
            Fragment: The newly created Fragment object.
        '''
        super().__init__(R)
        self.external = []

    def add_external(self,vertex):
        '''
        Adds a single external vertex to the fragment

        Args:
            vertex: The vertex to be appended to the list of external nodes
        '''
        if vertex.label in {v.label for v in self.external}:
            raise RuntimeError("vertex already marked")

        self.external.append(vertex)

    def nonterminals(self, NT):
        '''
        Returns a list of nonterminals that are edge labes of the fragment
        and can be identified by a list of all nonterminals used

        Args:
            NT (list): A list of all labels considered to be nonterminals in the grammar

        Returns:
            ntList (list): A list of nonterminals present in the provided list NT
            as well as in the list of all edge labels of the fragement
        '''
        ntlist = []
        for e in self.E:
            if e.label in NT:
                ntlist.append(e.label)
        return ntlist

    def createEdge(self, content,label,targets, semiring=None):
        '''
        Adds a single edge to the factorgraph

        Args:
            content: The content of the edge to be added
            label: The label of the newly added edge
            targets (set): A set of target vertices of the new edge
            f (Factorfunction): The function of the edge that is to be added
            semiring (semiring): The class of the semiring over which the vertices are defined
        '''
        e = FGEdge(content,label, semiring, None)
        for t in targets:
            e.add_target(t)
        return e

    def createFragment(self, vertexSet, edgeSet, external, semiring=None): # redundant
        '''
        Compare to the createFragment methon in fgglib/autotesting/testenvironment
        '''
        frag = Fragment(semiring)
        for v in vertexSet:
            frag.add_vertex(v)
        for e in edgeSet:
            frag.add_edge(e)
        for ext in external:
            frag.add_external(ext)
        return frag

    def buildFragment(self, V, E, ext, semiring=None): # redundant
        '''
        Compare to the buildFragment methon in fgglib/autotesting/testenvironment
        '''
        vertexDict = {l: FGVertex(None,l,semiring,VariableDomain(False)) for l in V}
        vertexSet = {v for i,v in vertexDict.items()}
        edgeSet = set()
        for tup in E:
            l = tup[0]
            s = tup[1]
            vs = [vertexDict[i] for i in s]
            edgeSet.add(self.createEdge(None,l,vs,semiring))
        external = {vertexDict[e] for e in ext}
        return self.createFragment(vertexSet, edgeSet, external, semiring)

    def __eq__(self,other):
        return self.external == other.external and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self):
        return super().__repr__()+"|X"+str(hash(frozenset(self.external)))

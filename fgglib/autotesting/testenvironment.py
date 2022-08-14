from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.fragment import Fragment
from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.fg.variabledomain import VariableDomain
from fgglib.base.semiring import *

def createEdge(content,label,targets): # add this as a classmethod alternatively
    """
    creates an edge from a list of targets and a label

    Args:
        label: the label the edge is supposed to have
        targets (list): a list of vertices that the edge connects

    Returns:
        e (Edge): The constructed edge
    """
    e = Edge(content,label)
    for t in targets:
        e.add_target(t)
    return e

def createFGEdge(content,label,targets, semiring=None):
    """
    creates a factor graph edge from a list of targets, a label and a semiring

    Args:
        label (list): the label the edge is supposed to have
        targets (list): a list of vertices that the edge connects
        semiring (semiring): the semiring on which the edge is defined

    Returns:
        e (Edge): The constructed edge
    """
    e = FGEdge(content,label,semiring, None)
    for t in targets:
        e.add_target(t)
    return e

def createFragment(vertexList, edgeList, external, semiring=None):
    """
    creates a factor graph fragment from a list of vertices, edges and external nodes

    Args:
        vertexSet (list): a list of vertices of the fragment to be constructed
        edgeSet (list): a list of edges of the fragment to be constructed
        semiring (semiring): the semiring on which the fragment is defined

    Returns:
        frag (Fragment): The constructed fragment
    """
    frag = Fragment(semiring)
    for v in vertexList:
        frag.add_vertex(v)
    for e in edgeList:
        frag.add_edge(e)
    for ext in external:
        frag.add_external(ext)
    return frag

def createFGGraph(vertexList, edgeList, semiring):
    """
    creates a factor graph from a list of vertices, edges and external nodes

    Args:
        vertexSet (list): a list of vertices of the fragment to be constructed
        edgeSet (list): a list of edges of the fragment to be constructed
        semiring (semiring): the semiring on which the fragment is defined

    Returns:
        fg (Factorgraph): The constructed factorgraph
    """
    fg = Factorgraph(semiring)
    for v in vertexList:
        fg.add_vertex(v)
    for e in edgeList:
        fg.add_edge(e)
    return fg

def buildGraph(V, E, semiring): # prohibits use of label multiple times
    """
    creates a factor graph from a list of labels for edges and vertices by
    constructing a list of vertices and edges and calling createFGGraph()

    Args:
        V (list): a list of vertex labels to be included in the graph
        E (dict): a list of edge mappings for the graph
        semiring (semiring): the semiring on which the fragment is defined

    Returns:
        Factorgraph: The constructed factorgraph
    """
    vertexDict = {l: FGVertex(None,l,semiring,defaultDomain) for l in V}
    vertexSet = {v for l,v in vertexDict.items()}
    edgeSet = set()
    for l,s in E.items():
        vs = [vertexDict[i] for i in s]
        edgeSet.add(createFGEdge(None,l,vs,semiring))
    return createFGGraph(vertexSet, edgeSet, semiring)

def buildFragment(V, E, ext, semiring=None): # prohibits use of vertex label multiple times
    """
    creates a factor graph fragment from a list of labels for edges and vertices by
    constructing a list of vertices and edges and calling createFGGraph()

    Args:
        V (list): a list of vertex labels to be included in the graph
        E (dict): a list of edge mappings for the graph
        ext (list): a list of vertices that should be considered external
        semiring (semiring): the semiring on which the fragment is defined

    Returns:
        Fragment: The constructed factorgraph fragment
    """
    vertexDict = {l: FGVertex(None,l,semiring,defaultDomain) for l in V}
    vertexSet = {v for i,v in vertexDict.items()}
    edgeSet = set()
    for tup in E:
        l = tup[0]
        s = tup[1]
        vs = [vertexDict[i] for i in s]
        edgeSet.add(createFGEdge(None,l,vs,semiring))
    external = {vertexDict[e] for e in ext}
    return createFragment(vertexSet, edgeSet, external, semiring)

defaultDomain = VariableDomain(False)
defaultDomain.set_content({0.25,0.5,0.75})
singularDomain = VariableDomain(False)
singularDomain.set_content({0.5})

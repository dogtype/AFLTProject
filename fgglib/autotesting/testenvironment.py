from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.fragment import Fragment
from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.fg.variabledomain import VariableDomain
from fgglib.base.semiring import *

def createEdge(content,label,targets): # add this as a classmethod alternatively
    e = Edge(content,label)
    for t in targets:
        e.add_target(t)
    return e

def createFGEdge(content,label,targets, semiring):
    e = FGEdge(content,label,semiring, None)
    for t in targets:
        e.add_target(t)
    return e

def createFragment(vertexSet, edgeSet, external):
    frag = Fragment()
    for v in vertexSet:
        frag.add_vertex(v)
    for e in edgeSet:
        frag.add_edge(e)
    for ext in external:
        frag.add_external(ext)
    return frag

def createFGGraph(vertexSet, edgeSet, semiring):
    fg = Factorgraph(semiring)
    for v in vertexSet:
        fg.add_vertex(v)
    for e in edgeSet:
        fg.add_edge(e)
    return fg

def buildGraph(V, E, semiring): # prohibits use of label multiple times
    vertexDict = {l: FGVertex(None,l,semiring,defaultDomain) for l in V}
    vertexSet = {v for l,v in vertexDict.items()}
    edgeSet = set()
    for l,s in E.items():
        vs = {vertexDict[i] for i in s}
        edgeSet.add(createFGEdge(None,l,vs,semiring))
    return createFGGraph(vertexSet, edgeSet, semiring)

def buildFragment(V, E, ext): # prohibits use of vertex label multiple times
    vertexDict = {l: Vertex(None,l) for l in V}
    vertexSet = {v for i,v in vertexDict.items()}
    edgeSet = set()
    for tup in E:
        l = tup[0]
        s = tup[1]
        vs = {vertexDict[i] for i in s}
        edgeSet.add(createEdge(None,l,vs))
    external = {vertexDict[e] for e in ext}
    return createFragment(vertexSet, edgeSet, external)

defaultDomain = VariableDomain(False)
defaultDomain.set_content({0.25,0.5,0.75})

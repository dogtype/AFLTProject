from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.base.semiring import *
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS ---------------------------------------

e1 = createEdge(None, 'e1', [Vertex(None,'V1'),Vertex(None,'V2')])
e2 = createFGEdge(None, 'e2', [FGVertex(None,'V1',Real,defaultDomain),FGVertex(None,'V2',Real,defaultDomain)], Real)
e3 = createEdge(None,'e3',set())

#-------------------------------- TESTS ----.-----------------------------------

def test_add_target1():
    '''
    Testing the add target function for a simple example of a Hypergraph
    '''
    e1.add_target(Vertex(None,'V3'))
    assert e1==createEdge(None, 'e1', [Vertex(None,'V1'),Vertex(None,'V2'),Vertex(None,'V3')])

def test_add_target2():
    '''
    Testing the add target function for a simple example of a Factorgraph
    '''
    e2.add_target(FGVertex(None,'V3',Real,defaultDomain))
    assert e2==createFGEdge(None, 'e2', [FGVertex(None,'V1',Real,defaultDomain),FGVertex(None,'V2',Real,defaultDomain),FGVertex(None,'V3',Real,defaultDomain)], Real)

def test_add_target3():
    '''
    Testing the add target function for an example of an empty Hypergraph
    '''
    e3.add_target(Vertex(None,'V1'))
    assert e3==createEdge(None,'e3',[Vertex(None,'V1')])

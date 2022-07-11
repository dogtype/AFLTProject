from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.base.semiring import *
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS ---------------------------------------

e1 = createEdge(None, 'e1', [Vertex(None,'V1'),Vertex(None,'V2')])
e2 = createFGEdge(None, 'e2', [FGVertex(None,'V1',Real),FGVertex(None,'V2',Real)], Real)
e3 = createEdge(None,'e3',set())

#-------------------------------- TESTS ----.-----------------------------------

def test_add_target1():
    e1.add_target(Vertex(None,'V3'))
    assert e1==createEdge(None, 'e1', [Vertex(None,'V1'),Vertex(None,'V2'),Vertex(None,'V3')])

def test_add_target2():
    e2.add_target(FGVertex(None,'V3',Real))
    assert e2==createFGEdge(None, 'e2', [FGVertex(None,'V1',Real),FGVertex(None,'V2',Real),FGVertex(None,'V3',Real)], Real)

def test_add_target3():
    e3.add_target(Vertex(None,'V1'))
    assert e3==createEdge(None,'e3',[Vertex(None,'V1')])

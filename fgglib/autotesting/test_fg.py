from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.fragment import Fragment
from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.base.semiring import *
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS ---------------------------------------

# Example 3 from Chiang, David, and Darcey, Riley. "Factor Graph Grammars." (2020).
# BOS      ┌──────┐             ┌──────┐              ┌──────┐             ┌──────┐            ┌──────┐     EOS
# ┌──┐     │      │     ┌──┐    │      │     ┌──┐     │      │     ┌──┐    │      │     ┌──┐   │      │     ┌──┐
# │  ├─────┤  T0  ├─────┤  ├────┤  T1  ├─────┤  ├─────┤  T3  ├─────┤  ├────┤  T5  ├─────┤  ├───┤  T7  ├─────┤  │
# └──┘     │      │     └──┘    │      │     └──┘     │      │     └──┘    │      │     └──┘   │      │     └──┘
#          └──────┘             └──┬───┘              └──┬───┘             └──┬───┘            └──────┘
#                                  │                     │                    │
#                                 ┌┴─┐                  ┌┴─┐                 ┌┴─┐
#                                 │  │                  │  │                 │  │
#                                 └┬─┘                  └┬─┘                 └┬─┘
#                                  │                     │                    │
#                               ┌──┴───┐              ┌──┴───┐             ┌──┴───┐
#                               │      │              │      │             │      │
#                               │  W2  │              │  W4  │             │  W6  │
#                               │      │              │      │             │      │
#                               └──────┘              └──────┘             └──────┘
hmmFG = buildGraph(
    {'T0','T1','W2','T3','W4','T5','W6','T7'}, # V
    {'e0':{'T0'},'e1':{'T0','T1'},'e2':{'T1','W2'},'e3':{'T1','T3'},'e4':{'T3','W4'},'e5':{'T3','T5'},
     'e6':{'T5','W6'},'e7':{'T5','T7'},'e8':{'T7'}}, # E,
    Real # R
)

# Figure 4.1 from Wymeersch, H. (2007). Factor graphs and the sum–product algorithm.
spaFG = buildGraph(
    {'X1','X2','X3','X4'}, # V
    {'fA':{'X1'},'fB':{'X1','X2'},'fC':{'X1','X2','X3'}}, # E,
    Real
)

frag1 = buildFragment(
    {'EXT1', 'EXT2'},
    {'N': {'EXT1','EXT2'}}, # V
    {'EXT1','EXT2'}, # ext
)

frag2 = buildFragment(
    {'EXT1', 'EXT2', 'V1', 'V3'}, # V
    {'N': {'EXT1','EXT2'}, 'M': {'EXT2','V1'}, 'K': {'V1','V3'}, 'V': {'EXT1','EXT2','V1'}, 'X': {'EXT1'}}, # E
    {'EXT1','EXT2'} # ext
)

cyclicFG = buildGraph(
    {'X1','X2','X3'},
    {'e1':{'X1','X2'},'e2':{'X2','X3'},'e3':{'X3','X1'}},
    Real
)

e1 = createEdge(None, 'e1', {Vertex(None,'V1'),Vertex(None,'V2')})
e2 = createFGEdge(None, 'e2', {FGVertex(None,'V1',Real),FGVertex(None,'V2',Real)}, Real)
e3 = createEdge(None,'e3',set())

# taken from https://github.com/danbar/fglib/blob/master/examples/example_spa
# A simple example of the sum-product algorithm
#
# This is a simple example of the sum-product algorithm on a factor graph
# with Bernoulli random variables, which is taken from page 409 of the book
# C. M. Bishop, Pattern Recognition and Machine Learning. Springer, 2006.
#
#       /--\      +----+      /--\      +----+      /--\
#      | x1 |-----| fa |-----| x2 |-----| fb |-----| x3 |
#       \--/      +----+      \--/      +----+      \--/
#                              |
#                            +----+
#                            | fc |
#                            +----+
#                              |
#                             /--\
#                            | x4 |
#                             \--/
#
# The following joint distributions are used for the factor nodes.
#
#      fa   | x2=0 x2=1     fb   | x3=0 x3=1     fc   | x4=0 x4=1
#      ----------------     ----------------     ----------------
#      x1=0 | 0.3  0.4      x2=0 | 0.3  0.4      x2=0 | 0.3  0.4
#      x1=1 | 0.3  0.0      x2=1 | 0.3  0.0      x2=1 | 0.3  0.0
#
spaFG = buildGraph(
    {'X1','X2','X3','X4'},
    {'fa':{'X1','X2'},'fb':{'X2','X3'},'fc':{'X2','X4'}},
    Real
)

#-------------------------------- TESTS ----.-----------------------------------


def test_sum_product1():
    #spaFG.sum_product()[spaFG.get_vertex('X4')] # calculate belief for node X4
    # How to define the necessary functions? Should I instantiate new derived classes from Factorfunction?
    assert True

def test_cyclic1():
    assert hmmFG.cyclic() == False

def test_cyclic2():
    assert cyclicFG.cyclic() == True

def test_add_target1():
    e1.add_target(Vertex(None,'V3'))
    assert e1==createEdge(None, 'e1', {Vertex(None,'V1'),Vertex(None,'V2'),Vertex(None,'V3')})

def test_add_target2():
    e2.add_target(FGVertex(None,'V3',Real))
    assert e2==createFGEdge(None, 'e2', {FGVertex(None,'V1',Real),FGVertex(None,'V2',Real),FGVertex(None,'V3',Real)}, Real)

def test_add_target3():
    e3.add_target(Vertex(None,'V1'))
    assert e3==createEdge(None,'e3',{Vertex(None,'V1')})

def test_leaves1():
    assert hmmFG.leaves()=={FGVertex(None,'W2',Real),FGVertex(None,'W4',Real),FGVertex(None,'W6',Real)}

def test_leaves2():
    assert frag1.leaves()=={Vertex(None,'EXT1'),Vertex(None,'EXT2')}

def test_leaves3():
    assert frag2.leaves()=={Vertex(None,'V3')}

def test_nonterminals1():
    assert frag1.nonterminals({'A'})==set()
    assert frag1.nonterminals({'N'})=={'N'}

def test_nonterminals2():
    assert frag2.nonterminals(set())==set()
    assert frag2.nonterminals({'N','M','Y'})=={'N','M'}
    assert frag2.nonterminals({'X','Y','V'})=={'X','V'}
    assert frag2.nonterminals({'N','M','K','V','X'})=={'N','M','K','V','X'}

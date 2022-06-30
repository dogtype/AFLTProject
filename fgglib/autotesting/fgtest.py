from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.fragment import Fragment
from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.base.semiring import *
from fgglib.autotesting.testenvironment import *


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
#
## Figure 3 from Chiang, David, and Darcey, Riley. "Factor Graph Grammars." (2020)., using only specific production rules
#conFG = createGraph( # not completed yet. I need to write this down first
#    {0:'T0',1:'T1',2:'W2',3:'T3',4:'W4',5:'T5',6:'W6',7:'T7'}, # V
#    {'e0':{0},'e1':{0,1},'e2':{1,2},'e3':{1,3},'e4':{3,4},'e5':{3,5},
#     'e6':{4,6},'e7':{4,7},'e8':{7}}, # E
#    Real # R
#)

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

e1 = createEdge(None, 'e1', {Vertex(None,'V1'),Vertex(None,'V2')})
e2 = createFGEdge(None, 'e2', {FGVertex(None,'V1',Real),FGVertex(None,'V2',Real)}, Real)
e3 = createEdge(None,'e3',set())

def test_sum_product():
    # use the example of fglib for this
    assert True

def test_add_target():
    e1.add_target(Vertex(None,'V3'))
    assert e1==createEdge(None, 'e1', {Vertex(None,'V1'),Vertex(None,'V2'),Vertex(None,'V3')})

    e2.add_target(FGVertex(None,'V3',Real))
    assert e2==createFGEdge(None, 'e2', {FGVertex(None,'V1',Real),FGVertex(None,'V2',Real),FGVertex(None,'V3',Real)}, Real)

    e3.add_target(Vertex(None,'V1'))
    assert e3==createEdge(None,'e3',{Vertex(None,'V1')})

def test_leaves():
    assert hmmFG.leaves()=={FGVertex(None,'W2',Real),FGVertex(None,'W4',Real),FGVertex(None,'W6',Real)}

    assert frag1.leaves()=={Vertex(None,'EXT1'),Vertex(None,'EXT2')}

    assert frag2.leaves()=={Vertex(None,'V3')}

def test_nonterminals():
    assert frag1.nonterminals({'A'})==set()
    assert frag1.nonterminals({'N'})=={'N'}

    assert frag2.nonterminals(set())==set()
    assert frag2.nonterminals({'N','M','Y'})=={'N','M'}
    assert frag2.nonterminals({'X','Y','V'})=={'X','V'}
    assert frag2.nonterminals({'N','M','K','V','X'})=={'N','M','K','V','X'}

from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge
from fgglib.base.semiring import Real

def createGraph(V, E, semiring): # maybe use labeling instead of an index, but this doesn't support same label on different vertices
    vertexDict = {n: Vertex(None,l) for n,l in V.items()}
    vertexSet = {v for i,v in vertexDict.items()}
    edgeSet = set()
    for l,s in E.items():
        vs = {vertexDict[i] for i in s}
        edgeSet.add(Edge(None,l,vs))
    return Factorgraph(vertexSet, edgeSet, semiring)

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
#                               │  T2  │              │  T4  │             │  T6  │
#                               │      │              │      │             │      │
#                               └──────┘              └──────┘             └──────┘
hmmFG = createGraph(
    {0:'T0',1:'T1',2:'W2',3:'T3',4:'W4',5:'T5',6:'W6',7:'T7'}, # V
    {'e0':{0},'e1':{0,1},'e2':{1,2},'e3':{1,3},'e4':{3,4},'e5':{3,5},
     'e6':{5,6},'e7':{5,7},'e8':{7}}, # E,
    Real # R
)



def test_print():
    print(hmmFG)
    hmmFG.draw()

test_print()

from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.vertex import Vertex
from fgglib.fg.edge import Edge
from fgglib.base.semiring import Real
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


def test_print():
    print(hmmFG)
    hmmFG.draw()

test_print()

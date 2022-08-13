from fgglib.fg.factorgraph import Factorgraph
from fgglib.fg.fragment import Fragment
from fgglib.fg.vertex import Vertex, FGVertex
from fgglib.fg.edge import Edge, FGEdge
from fgglib.base.semiring import *
from fgglib.autotesting.testenvironment import *
from fgglib.fg.functions.discretedensity import DiscreteDensity
from fgglib.fg.functions.tropicalmul import TropicalMul

#--------------------------- DEFINITIONS ---------------------------------------

hmmFG = buildGraph(
    {'T0','T1','W2','T3','W4','T5','W6','T7'}, # V
    {'e0':{'T0'},'e1':{'T0','T1'},'e2':{'T1','W2'},'e3':{'T1','T3'},'e4':{'T3','W4'},'e5':{'T3','T5'},
     'e6':{'T5','W6'},'e7':{'T5','T7'},'e8':{'T7'}}, # E,
    Real # R
)

frag1 = buildFragment(
    {'EXT1', 'EXT2'},
    [('N', {'EXT1','EXT2'})], # V
    {'EXT1','EXT2'}, # ext

)

frag2 = buildFragment(
    {'EXT1', 'EXT2', 'V1', 'V3'}, # V
    [('N', {'EXT1','EXT2'}), ('M', {'EXT2','V1'}), ('K', {'V1','V3'}), ('V', {'EXT1','EXT2','V1'}), ('X', {'EXT1'})], # E
    {'EXT1','EXT2'} # ext
)

cyclicFG = buildGraph(
    {'X1','X2','X3'},
    {'e1':{'X1','X2'},'e2':{'X2','X3'},'e3':{'X3','X1'}},
    Real
)

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
#      fa   | x2=0 x2=1 x2=2     fb   | x3=0 x3=1     fc   | x4=0 x4=1
#      ---------------------     ----------------     ----------------
#      x1=0 | 0.3  0.2  0.1      x2=0 | 0.3  0.2      x2=0 | 0.3  0.2
#      x1=1 | 0.3  0.0  0.1      x2=1 | 0.3  0.0      x2=1 | 0.3  0.0
#                                x2=2 | 0.1  0.1      x2=2 | 0.1  0.1

spaFG1 = buildGraph(
    ['X1','X2','X3','X4'],
    {'fa':['X1','X2'],'fb':['X2','X3'],'fc':['X2','X4']},
    Real
)

spaFG2 = buildGraph(
    ['X1','X2','X3','X4'],
    {'fa':['X1','X2'],'fb':['X2','X3','X4']},
    Tropical
)

#-------------------------------- TESTS ----------------------------------------

def test_sum_product1():
    d1 = VariableDomain(False)
    d1.set_content({0,1})
    d2 = VariableDomain(False)
    d2.set_content({0,1,2})
    spaFG1.get_vertex('X1').domain = d1
    spaFG1.get_vertex('X2').domain = d2
    spaFG1.get_vertex('X3').domain = d1
    spaFG1.get_vertex('X4').domain = d1
    
    spaFG1.set_function(spaFG1.get_edge('fa'), DiscreteDensity([[0.3, 0.2, 0.1],[0.3, 0, 0.1]]))
    spaFG1.set_function(spaFG1.get_edge('fb'), DiscreteDensity([[0.3, 0.2],[0.3, 0],[0.1, 0.1]]))
    spaFG1.set_function(spaFG1.get_edge('fc'), DiscreteDensity([[0.3, 0.2],[0.3, 0],[0.1, 0.1]]))

    marginals = spaFG1.sum_product()
    m1 = marginals[spaFG1.get_vertex('X1')]
    m2 = marginals[spaFG1.get_vertex('X2')]
    m3 = marginals[spaFG1.get_vertex('X3')]
    m4 = marginals[spaFG1.get_vertex('X4')]
    assert np.allclose(np.asarray([m1.compute(0).score, m1.compute(1).score]) / m1.normalization_constant(d1).score, [0.551136, 0.448863], atol=1e-3)
    assert np.allclose(np.asarray([m2.compute(0).score, m2.compute(1).score, m2.compute(2).score]) / m2.normalization_constant(d2).score, [0.852272, 0.102272, 0.045454], atol=1e-3)
    assert np.allclose(np.asarray([m3.compute(0).score, m3.compute(1).score]) / m3.normalization_constant(d1).score, [0.636363, 0.363636], atol=1e-3)
    assert np.allclose(np.asarray([m4.compute(0).score, m4.compute(1).score]) / m3.normalization_constant(d1).score, [0.636363, 0.363636], atol=1e-3)
    
def test_normalization_constant1():
    d1 = VariableDomain(False)
    d1.set_content({0,1})
    d2 = VariableDomain(False)
    d2.set_content({0,1,2})
    spaFG1.get_vertex('X1').domain = d1
    spaFG1.get_vertex('X2').domain = d2
    spaFG1.get_vertex('X3').domain = d1
    spaFG1.get_vertex('X4').domain = d1
    
    spaFG1.set_function(spaFG1.get_edge('fa'), DiscreteDensity([[0.3, 0.2, 0.1],[0.3, 0, 0.1]]))
    spaFG1.set_function(spaFG1.get_edge('fb'), DiscreteDensity([[0.3, 0.2],[0.3, 0],[0.1, 0.1]]))
    spaFG1.set_function(spaFG1.get_edge('fc'), DiscreteDensity([[0.3, 0.2],[0.3, 0],[0.1, 0.1]]))
    
    assert np.allclose(float(spaFG1.normalization_constant().score), 0.176, atol=1e-3)
    
    
def test_sum_product2():
    d1 = VariableDomain(False)
    d1.set_content({1,2,3})
    d2 = VariableDomain(False)
    d2.set_content({4,5})
    d3 = VariableDomain(False)
    d3.set_content({6})
    d4 = VariableDomain(False)
    d4.set_content({7,8})
    spaFG2.get_vertex('X1').domain = d1
    spaFG2.get_vertex('X2').domain = d2
    spaFG2.get_vertex('X3').domain = d3
    spaFG2.get_vertex('X4').domain = d4
    
    spaFG2.set_function(spaFG2.get_edge('fa'), TropicalMul(2))
    spaFG2.set_function(spaFG2.get_edge('fb'), TropicalMul(3))
    
    marginals = spaFG2.sum_product()
    assert np.allclose(marginals[spaFG2.get_vertex('X1')].compute(1).score, 22, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X1')].compute(2).score, 23, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X1')].compute(3).score, 24, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X2')].compute(4).score, 22, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X2')].compute(5).score, 24, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X3')].compute(6).score, 22, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X4')].compute(7).score, 22, atol=1e-3)
    assert np.allclose(marginals[spaFG2.get_vertex('X4')].compute(8).score, 23, atol=1e-3)
    
def test_normalization_constant2():
    d1 = VariableDomain(False)
    d1.set_content({1,2,3})
    d2 = VariableDomain(False)
    d2.set_content({4,5})
    d3 = VariableDomain(False)
    d3.set_content({6})
    d4 = VariableDomain(False)
    d4.set_content({7,8})
    spaFG2.get_vertex('X1').domain = d1
    spaFG2.get_vertex('X2').domain = d2
    spaFG2.get_vertex('X3').domain = d3
    spaFG2.get_vertex('X4').domain = d4
    
    spaFG2.set_function(spaFG2.get_edge('fa'), TropicalMul(2))
    spaFG2.set_function(spaFG2.get_edge('fb'), TropicalMul(3))
    
    assert spaFG2.normalization_constant().score == 22
    
def test_sum_product3():
    # set domains
    # set functions (normals)
    pass

def test_normalization_constant3():
    # set domains
    # set functions (normals)
    pass

def test_cyclic1():
    assert hmmFG.cyclic() == False

def test_cyclic2():
    assert cyclicFG.cyclic() == True

def test_leaves1():
    assert hmmFG.leaves()=={FGVertex(None,'W2',Real,defaultDomain),FGVertex(None,'W4',Real,defaultDomain),FGVertex(None,'W6',Real,defaultDomain)}

def test_leaves2():
    assert frag1.leaves()=={FGVertex(None,'EXT1',frag1.R, VariableDomain(False)),FGVertex(None,'EXT2',frag1.R, VariableDomain(False))}

def test_leaves3():
    assert frag2.leaves()=={FGVertex(None,'V3',frag2.R, VariableDomain(False))}

def test_nonterminals1():
    assert set(frag1.nonterminals({'A'}))==set()
    assert set(frag1.nonterminals({'N'}))=={'N'}

def test_nonterminals2():
    assert set(frag2.nonterminals(set()))==set()
    assert set(frag2.nonterminals({'N','M','Y'}))=={'N','M'}
    assert set(frag2.nonterminals({'X','Y','V'}))=={'X','V'}
    assert set(frag2.nonterminals({'N','M','K','V','X'}))=={'N','M','K','V','X'}
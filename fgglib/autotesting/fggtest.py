from fgglib.fgg.fgg import FGG
from fgglib.fg.fragment import Fragment

frag0 = Fragment(
    {0},
    {'e0','e1'},
    {'e0':{0},'e1':{0,'X'}},
    {0:'T1'},
    {'e0':'BOS'} # have to introduce nonterminals as edge labels
    #{}, # omega
    #{} # phi
)

frag1 = Fragment(
    {0},
    {'e0','e1'},
    {'e0':{0},'e1':{0,'X'}},
    {0:'T1'},
    {'e0':'BOS'} # have to introduce nonterminals as edge labels
    #{}, # omega
    #{} # phi
)

frag2 = Fragment(
    {0},
    {'e0','e1'},
    {'e0':{0},'e1':{0,'X'}},
    {0:'T1'},
    {'e0':'BOS'} # have to introduce nonterminals as edge labels
    #{}, # omega
    #{} # phi
)

hmmFGG = FGG(
    {frag0,frag1,frag2},
    {'X','X','S'},
    'S',
    {('S', frag0),
     ('X', frag1),
     ('X', frag2)}
)

def test_recursive_example():
    assert True

def test_linearly_recursive_example():
    assert True

def test_reentrant_examle():
    assert True

def test_size_example():
    assert True

def test_cyclic_example():
    assert True

def test_conjunction_example():
    assert True

def test_inference_finite_variables_example():
    assert True

def test_inference_finite_states_example():
    assert True

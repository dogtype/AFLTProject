from fgglib.fgg.fgg import FGG
from fgglib.fg.fragment import Fragment
from fgglib.fgg.production import *
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS --------------------------------------

recFrag0 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    {'X': {'EXT1','EXT2'}}, # E
    {'EXT1','EXT2'}, # ext
)

recFrag1 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    {'l': {'EXT1','EXT2'}}, # E
    {'EXT1','EXT2'}, # ext
)

recFGG = FGG(
    {recFrag0, recFrag1}, # T
    {'S','X'}, # N
    {'S'}, # S
    {Production('S',recFrag0),
     Production('X',recFrag0),
     Production('X',recFrag1)} # P
)

#hmmFGG = FGG(
#    {frag0,frag1,frag2},
#    {'X','X','S'},
#    'S',
#    {('S', frag0),
#     ('X', frag1),
#     ('X', frag2)}
#)

addFGG = FGG(
    set(),
    {'S'},
    {'S'},
    set()
)

frag1 = buildFragment(
    {'T1', 'T2'}, # V
    {'P': {'T1','T2'}, 'EOS': {'T2'}}, # E
    {'T1'} # ext
)

frag2 = buildFragment(
    {'T1','T2'}, # V
    {}, # E
    {'T1'} # ext
)

frag3 = buildFragment(
    {'T1'},
    {'BOS':{'T1'},'X2':{'T1'}},
    {}
)

frag4 = buildFragment(
    {'T1'},
    {'(0)2':{'T1'}},
    {}
)

frag5 = buildFragment(
    {'T1'},
    {'BOS':{'T1'},('X2','(0)2'):{'T1'}},
    {}
)

frag6 = buildFragment(
    {'T1','T2','W3'},
    {'P21':{'T1','T2'},'P32':{'T2','W3'},'X4':{'T2'}},
    {'T1'}
)

frag7 = buildFragment(
    {'T1','T2','W3'},
    {'(i)4':{'T2'},'wi':{'W3'}},
    {'T1'}
)

frag8 = buildFragment(
    {'T1','T2','W3'},
    {'P21':{'T1','T2'},'P32':{'T2','W3'},('X4','(i)4'):{'T2'},'wi':{'W3'}},
    {'T1'}
)

prod0 = Production('X',frag1)
prod1 = Production('(n)',frag2)
prod2 = Production(('X','(n)'),frag1)

prod3 = Production('S',frag3)
prod4 = Production('S',frag4)
prod5 = Production(('S','S'),frag5)

prod6 = Production('X',frag6)
prod7 = Production('(i-1)',frag7)
prod8 = Production(('X','(i-1)'),frag8)

conFGG1 = FGG(
    {frag1,frag3,frag6}, # T
    {'S','X','X4','X2'}, # N
    {'S'}, # S
    {Production('X',frag1),
     Production('S',frag3),
     Production('X',frag6)} # P
)

conFGG2 = FGG(
    {frag2,frag4,frag7}, # T
    {'(n)','S','(i-1)','(i)4','(0)2'}, # N
    {'S'}, # S
    {Production('(n)',frag2),
     Production('S',frag4),
     Production('(i-1)',frag7)} # P
)

conFGG3 = FGG(
    {frag1,frag5,frag8}, # T
    {'(n)','X','X4','S','(i-1)','(i)4','X2','(0)2'}, # N
    {'S'}, # S
    {Production(('X','(n)'),frag1),
     Production(('S','S'),frag5),
     Production(('X','(i-1)'),frag8)} # P
)

#-------------------------------- TESTS ----.-----------------------------------


def test_add_example1():
    addFGG.add('S',recFrag0)
    assert addFGG.nProductions('S')=={('S',recFrag0)}

def copy_exampl1e():
    newFGG = addFGG.copy()
    assert newFGG == addFGG

def test_nProductions_example1():
    assert recFGG.nProductions('X')=={('X',recFrag0),('X',recFrag1)}

def test_recursive_example1():
    assert True #recFGG.recursive()==True

def test_linearly_recursive_example1():
    assert True

def test_reentrant_example1():
    assert True# recFGG.reentrant()==False

def test_conjunction_example1():
    assert conFGG1.conjunction(conFGG2) == conFGG3

def test_inference_finite_variables_example1():
    assert True

def test_inference_finite_states_example1():
    assert True

test_conjunction_example1()

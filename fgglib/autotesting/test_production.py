from fgglib.fgg.fgg import FGG
from fgglib.fg.fragment import Fragment
from fgglib.fgg.production import *
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS ---------------------------------------

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
    {'BOS':{'T1'},('BOS','(0)2'):{'T1'}},
    {}
)

prod1 = Production('X',frag1)
prod2 = Production('(n)',frag2)
prod3 = Production(('X','(n)'),frag1)

prod4 = Production('S',frag3)
prod5 = Production('S',frag4)
prod6 = Production('S',frag5)

#-------------------------------- TESTS ----.-----------------------------------

def test_conjoinable1():
    assert prod1.conjoinable(prod2, {'X','(n)'})

def test_conjoinable2():
    assert prod4.conjoinable(prod5, {'S','(0)2','X2'})

def test_conjoin1():
    assert prod1.conjoin(prod2, {'X','(n)'}) == prod3

def test_conjoin2():
    print(prod4.conjoin(prod5, {'S','(0)2','X2'}))

test_conjoin2()

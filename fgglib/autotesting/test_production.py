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

#-------------------------------- TESTS ----.-----------------------------------

def test_conjoinable1():
    assert prod0.conjoinable(prod1, {'X','(n)'})

def test_conjoinable2():
    assert prod3.conjoinable(prod4, {'S','(0)2','X2'})

def test_conjoinable3():
    assert prod6.conjoinable(prod7, {'(i-1)','(i)4','X4'})

def test_conjoin1():
    assert prod0.conjoin(prod1, {'X','(n)'}) == prod2

def test_conjoin2():
    assert prod3.conjoin(prod4, {'S','(0)2','X2'}) == prod5

def test_conjoin3():
    assert prod6.conjoin(prod7, {'(i-1)','(i)4','X4'}) == prod8

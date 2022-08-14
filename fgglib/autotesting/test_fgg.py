from fgglib.fgg.fgg import FGG
from fgglib.fg.fragment import Fragment
from fgglib.fgg.production import *
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS --------------------------------------

recFrag0 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    [('X', {'EXT1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

recFrag1 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    [('l', {'EXT1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

recFrag2 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    [('S', {'EXT1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

recFrag3 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    [('m', {'EXT1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

recFGG = FGG(
    {recFrag0, recFrag1}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',recFrag0),
     Production('X',recFrag1)} # P
)

nonRecFGG = FGG(
    {recFrag0, recFrag1}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',recFrag1)} # P
)

nonlinRecFrag1 = buildFragment(
    {'EXT1', 'EXT2', 'v1'}, # V
    [('X', {'EXT1','v1'}), ('X',{'v1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

nonlinRecFrag2 = buildFragment(
    {'EXT1', 'EXT2', 'v1'}, # V
    [('Y', {'EXT1','v1'}), ('Y',{'v1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

nonlinRecFrag3 = buildFragment(
    {'EXT1', 'EXT2', 'v1'}, # V
    [('Y', {'EXT1','v1'}), ('X',{'v1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

nonlinRecFGG = FGG(
    {recFrag0, recFrag1, nonlinRecFrag1}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag1),
     Production('X',recFrag1)} # P
)

nonlinRecFGG2 = FGG(
    {recFrag0, recFrag1, nonlinRecFrag2}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag2),
     Production('X',recFrag1),
     Production('Y',recFrag0)} # P
)

nonlinRecFGG3 = FGG(
    {recFrag0, recFrag1, nonlinRecFrag2}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag2),
     Production('Y',recFrag1)} # P
)

nonlinRecFGG4 = FGG(
    {recFrag0, recFrag1, nonlinRecFrag3}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',recFrag1),
     Production('X',nonlinRecFrag3),
     Production('Y',recFrag0)} # P
)

nonlinRecFGG5 = FGG(
    {recFrag0, recFrag1, recFrag2, nonlinRecFrag3}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',recFrag1),
     Production('X',nonlinRecFrag3),
     Production('Y',recFrag2)} # P
)

linRecFGG = FGG(
    {recFrag0, recFrag1, recFrag2, nonlinRecFrag2}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('S',recFrag1),
     Production('S',recFrag2),
     Production('X',recFrag0),
     Production('X',recFrag2),
     Production('X',recFrag1),
     Production('X',nonlinRecFrag2),
     Production('Y',recFrag1)} # P
)

nonReentFGG = FGG(
    {recFrag0, recFrag1, recFrag2, nonlinRecFrag2}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag2),
     Production('Y',recFrag1)} # P
)

reentFGG = FGG(
    {recFrag0, recFrag1, recFrag2, nonlinRecFrag2}, # T
    {'S','X','Y'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag2),
     Production('Y',recFrag1),
     Production('Y',recFrag3)} # P
)

addFGG = FGG(
    set(),
    {'S'},
    'S',
    set()
)

frag1 = buildFragment(
    {'T1', 'T2'}, # V
    [('P', {'T1','T2'}), ('EOS', {'T2'})], # E
    {'T1'} # ext
)

frag2 = buildFragment(
    {'T1','T2'}, # V
    [], # E
    {'T1'} # ext
)

frag3 = buildFragment(
    {'T1'},
    [('BOS',{'T1'}),('X2',{'T1'})],
    {}
)

frag4 = buildFragment(
    {'T1'},
    [('(0)2',{'T1'})],
    {}
)

frag5 = buildFragment(
    {'T1'},
    [('BOS',{'T1'}),(('X2','(0)2'),{'T1'})],
    {}
)

frag6 = buildFragment(
    {'T1','T2','W3'},
    [('P21',{'T1','T2'}),('P32',{'T2','W3'}),('X4',{'T2'})],
    {'T1'}
)

frag7 = buildFragment(
    {'T1','T2','W3'},
    [('(i)4',{'T2'}),('wi',{'W3'})],
    {'T1'}
)

frag8 = buildFragment(
    {'T1','T2','W3'},
    [('P21',{'T1','T2'}),('P32',{'T2','W3'}),(('X4','(i)4'),{'T2'}),('wi',{'W3'})],
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
    'S', # S
    {Production('X',frag1),
     Production('S',frag3),
     Production('X',frag6)} # P
)

conFGG2 = FGG(
    {frag2,frag4,frag7}, # T
    {'(n)','S','(i-1)','(i)4','(0)2'}, # N
    'S', # S
    {Production('(n)',frag2),
     Production('S',frag4),
     Production('(i-1)',frag7)} # P
)

conFGG3 = FGG(
    {frag1,frag5,frag8}, # T
    {'(n)','X','X4','S','(i-1)','(i)4','X2','(0)2'}, # N
    'S', # S
    {Production(('X','(n)'),frag1),
     Production(('S','S'),frag5),
     Production(('X','(i-1)'),frag8)} # P
)

#-------------------------------- TESTS ----.-----------------------------------


def test_add_example1():
    '''
    Testing the add function for FGGs on an example of an empty grammar
    '''
    addFGG.add('S',recFrag0)
    assert addFGG.nProductions('S')=={('S',recFrag0)}

def copy_example1():
    '''
    Testing the copy function for FGGs
    '''
    newFGG = addFGG.copy()
    assert newFGG == addFGG

def test_nProductions_example1():
    '''
    Testing the nProductions function for FGGs on a simple example of a recursive grammar
    '''
    assert recFGG.nProductions('X')=={('X',recFrag0),('X',recFrag1)}

def test_recursive_example1():
    '''
    Testing the recursive function on an example of a recursive FGG
    '''
    assert recFGG.recursive()==True

def test_recursive_example2():
    '''
    Testing the recursive function on an example of a simple nonrecursive FGG
    '''
    assert nonRecFGG.recursive()==False

def test_linearly_recursive_example1():
    '''
    Testing the linearly_recursive function on a simple example of a recursive FGG
    '''
    assert recFGG.linearly_recursive()==True

def test_linearly_recursive_example2():
    '''
    Testing the linearly_recursive function on an example of a recursive, but
    nonlinearly recursive factor graph grammar
    '''
    assert nonlinRecFGG.linearly_recursive()==False

def test_linearly_recursive_example3():
    '''
    Testing the linearly_recursive function on an example of a nonlinearly recursive grammar
    '''
    assert nonlinRecFGG2.linearly_recursive()==False

def test_linearly_recursive_example4():
    '''
    Testing the linearly_recursive function on an example of a nonlinearly recursive grammar
    '''
    assert nonlinRecFGG3.linearly_recursive()==False

def test_linearly_recursive_example5():
    '''
    Testing the linearly_recursive function on an example of a nonlinearly recursive grammar
    '''
    assert nonlinRecFGG4.linearly_recursive()==False

def test_linearly_recursive_example6():
    '''
    Testing the linearly_recursive function on an example of a nonlinearly recursive grammar
    '''
    assert nonlinRecFGG5.linearly_recursive()==False

def test_linearly_recursive_example7():
    '''
    Testing the linearly_recursive function on a different example of a linearly
    recursive grammar
    '''
    assert linRecFGG.linearly_recursive()==True

def test_diffDerivTree1():
    '''
    Testing the diffDerivTree function on a simple example of a recursive grammar
    '''
    assert recFGG.diffDerivTree()=={'S','X'}

def test_diffDerivTree2():
    '''
    Testing the diffDerivTree function on a simple example of a nonrecursive grammar
    '''
    assert nonRecFGG.diffDerivTree()==set()

def test_diffDerivTree3():
    '''
    Testing the diffDerivTree function on an example of a nonlinearly recursive grammar
    '''
    assert nonlinRecFGG.diffDerivTree()=={'S','X'}

def test_reentrant_example1():
    '''
    Testing the reentrant function on an example of a simple recursive FGG
    '''
    assert recFGG.reentrant()==True

def test_reentrant_example2():
    '''
    Testing the reentrant function on an example of a simple nonrecursive FGG
    '''
    assert nonRecFGG.reentrant()==False

def test_reentrant_example3():
    '''
    Testing the reentrant function on an example of an empty FGG
    '''
    assert addFGG.reentrant()==False

def test_reentrant_example4():
    '''
    Testing the reentrant predicate on an example of a specifically nonrecursive
    and nonreentrant FGG
    '''
    assert nonReentFGG.reentrant()==False

def test_reentrant_example5():
    '''
    Testing the reentrant predicate on an example of a specifically nonrecursive
    but reentrant FGG
    '''
    assert reentFGG.reentrant()==True

def test_conjunction_example1():
    '''
    Testing the conjunction algorithm on an example from Chiang, D., & Riley, D. (2020).
    Factor Graph Grammars. In Proc. NeurIPS (pp. 6648–6658).
    '''
    assert conFGG1.conjunction(conFGG2) == conFGG3

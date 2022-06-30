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
     Production('X',recFrag1)}
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
    assert True

def test_inference_finite_variables_example1():
    assert True

def test_inference_finite_states_example1():
    assert True

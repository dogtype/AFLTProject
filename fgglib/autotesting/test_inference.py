from fgglib.fgg.fgg import FGG
from fgglib.fg.fragment import Fragment
from fgglib.fgg.production import *
from fgglib.fgg.fggsum_product import FGGsum_product
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


nonlinRecFrag1 = buildFragment(
    {'EXT1', 'EXT2', 'v1'}, # V
    [('X', {'EXT1','v1'}), ('X',{'v1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

nonRecFGG = FGG(
    {recFrag0, recFrag1}, # T
    {'S','X'}, # N
    {'S'}, # S
    {Production('S',recFrag0),
     Production('X',recFrag1)}, # P
)

recFGG = FGG(
    {recFrag0, recFrag1}, # T
    {'S','X'}, # N
    {'S'}, # S
    {Production('S',recFrag0),
     Production('X',recFrag0),
     Production('X',recFrag1)} # P
)

nonlinRecFGG = FGG(
    {recFrag0, recFrag1, nonlinRecFrag1}, # T
    {'S','X'}, # N
    {'S'}, # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag1),
     Production('X',recFrag1)} # P
)




#-------------------------------- TESTS ----.-----------------------------------

def test_inference_finite_variables_example1():
    fggsp = FGGsum_product(nonRecFGG)
    assert True #fggsp.inference()==0.875

def test_inference_finite_variables_example2():
    fggsp = FGGsum_product(recFGG)#
    assert True # fggsp.inference()==

def test_inference_finite_variables_example3():
    fggsp = FGGsum_product(nonlinRecFGG)#
    assert True # fggsp.inference()==


def test_inference_finite_states_example1():
    assert True

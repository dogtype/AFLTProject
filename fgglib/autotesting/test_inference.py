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

recFragp = buildFragment(
    {'V'}, # V
    [('X', {'V','V'})], # E
    {}, # ext
)
recFragp.get_edge('X').add_target(recFragp.get_vertex('V'))

nonlinRecFrag1 = buildFragment(
    {'EXT1', 'EXT2', 'v1'}, # V
    [('X', {'EXT1','v1'}), ('X',{'v1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

nonRecFGG = FGG(
    {recFrag1, recFragp}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFragp),
     Production('X',recFrag1)}, # P
)
nonRecFGG.set_variable_domain('V',singularDomain)

recFGG = FGG(
    {recFrag0, recFrag1, recFragp}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFragp),
     Production('X',recFrag0),
     Production('X',recFrag1)} # P
)
recFGG.set_variable_domain('V',singularDomain)


nonlinRecFGG = FGG(
    {recFrag0, recFrag1, nonlinRecFrag1}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFrag0),
     Production('X',nonlinRecFrag1),
     Production('X',recFrag1)} # P
)
nonlinRecFGG.set_variable_domain('V',defaultDomain)





#-------------------------------- TESTS ----.-----------------------------------

def test_inference_finite_variables_example1():
    fggsp = FGGsum_product(nonRecFGG)
    assert fggsp.inference()==0.25

def test_inference_finite_variables_example2():
    nonRecFGG.set_variable_domain('V',defaultDomain)
    fggsp = FGGsum_product(nonRecFGG)
    assert fggsp.inference()==0.875

def test_inference_finite_variables_example3():
    fggsp = FGGsum_product(recFGG)
    assert fggsp.inference()==0.875

test_inference_finite_variables_example3()

def test_inference_finite_variables_example4():
    recFGG.set_variable_domain('V',defaultDomain)
    fggsp = FGGsum_product(recFGG)
    assert True#fggsp.inference()==

def test_inference_finite_variables_example5():
    fggsp = FGGsum_product(nonlinRecFGG)
    assert True # fggsp.inference()==


def test_inference_finite_states_example1():
    assert True

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
recFragp.get_edge('X').add_target(recFragp.get_vertex('V')) # workaround for edge assignment of the test environment

recFrag0p = buildFragment(
    {'EXT1', 'EXT2', 'V'}, # V
    [('X', {'EXT1','V'}),('b',{'V','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)

nonlinRecFrag1 = buildFragment(
    {'EXT1', 'EXT2', 'V'}, # V
    [('X', {'EXT1','V'}), ('X',{'V','EXT2'})], # E
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
nonRecFGG.set_variable_domain('EXT1',singularDomain)
nonRecFGG.set_variable_domain('EXT2',singularDomain)

recFGG = FGG(
    {recFrag0p, recFrag1, recFragp}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFragp),
     Production('X',recFrag0p),
     Production('X',recFrag1)} # P
)
recFGG.set_variable_domain('V',singularDomain)
recFGG.set_variable_domain('EXT1',singularDomain)
recFGG.set_variable_domain('EXT2',singularDomain)


nonlinRecFGG = FGG(
    {recFrag0, recFrag1, nonlinRecFrag1}, # T
    {'S','X'}, # N
    'S', # S
    {Production('S',recFragp),
     Production('X',nonlinRecFrag1),
     Production('X',recFrag1)} # P
)
nonlinRecFGG.set_variable_domain('V',singularDomain)
recFGG.set_variable_domain('EXT1',singularDomain)
recFGG.set_variable_domain('EXT2',singularDomain)



#-------------------------------- TESTS ----.-----------------------------------

def test_inference_finite_variables_example1():
    fggsp = FGGsum_product(nonRecFGG)
    assert fggsp.inference()==0.25

def test_inference_finite_variables_example2():
    nonRecFGG.set_variable_domain('V',defaultDomain)
    nonRecFGG.set_variable_domain('EXT1',defaultDomain)
    nonRecFGG.set_variable_domain('EXT2',defaultDomain)
    fggsp = FGGsum_product(nonRecFGG)
    assert fggsp.inference()==0.875

def test_inference_finite_variables_example3():
    fggsp = FGGsum_product(recFGG)
    assert fggsp.inference()==0.3333333333333333


def test_inference_finite_variables_example5():
    fggsp = FGGsum_product(nonlinRecFGG)
    assert True#fggsp.inference()==0.5


def test_inference_finite_states_example1():
    assert True

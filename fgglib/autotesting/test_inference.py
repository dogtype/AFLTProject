from fgglib.fgg.fgg import FGG
from fgglib.fg.fragment import Fragment
from fgglib.fgg.production import *
from fgglib.fgg.fggsum_product import FGGsum_product
from fgglib.base.semiring import Real
from fgglib.fg.functions.discretedensity import DiscreteDensity
from fgglib.fg.factorfunction import FactorFunction
from fgglib.autotesting.testenvironment import *

#--------------------------- DEFINITIONS --------------------------------------

class MultiplicativeFactorFunction(FactorFunction):
    def __init__(self):
        super().__init__(Real,1)

    def compute(self,*args):
        result = 1
        for a in args:
            result*=a
        return result

mff = MultiplicativeFactorFunction()

recFrag0 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    [('X', {'EXT1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)
for e in recFrag0.E:
    recFrag0.set_function(e,mff)

recFrag1 = buildFragment(
    {'EXT1', 'EXT2'}, # V
    [('l', {'EXT1','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)
for e in recFrag1.E:
    recFrag1.set_function(e,mff)

recFragp = buildFragment(
    {'V'}, # V
    [('X', {'V','V'})], # E
    {}, # ext
)
recFragp.get_edge('X').add_target(recFragp.get_vertex('V')) # workaround for edge assignment of the test environment
for e in recFragp.E:
    recFragp.set_function(e,mff)


recFrag0p = buildFragment(
    {'EXT1', 'EXT2', 'V'}, # V
    [('X', {'EXT1','V'}),('b',{'V','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)
for e in recFrag0p.E:
    recFrag0p.set_function(e,mff)

nonlinRecFrag1 = buildFragment(
    {'EXT1', 'EXT2', 'V'}, # V
    [('X', {'EXT1','V'}), ('X',{'V','EXT2'})], # E
    {'EXT1','EXT2'}, # ext
)
for e in nonlinRecFrag1.E:
    nonlinRecFrag1.set_function(e,mff)

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
nonlinRecFGG.set_variable_domain('EXT1',singularDomain)
nonlinRecFGG.set_variable_domain('EXT2',singularDomain)

finStatesFrag0 = buildFragment(
    ['A1', 'B2', 'A4'],
    [('X',['A1', 'B2', 'A4'])],
    {},
    Real
)

finStatesFrag1 = buildFragment(
    ['A1', 'B2'],
    [('Y',['A1', 'B2'])],
    {},
    Real
)

finStatesFrag2 = buildFragment(
    ['A1', 'B2', 'A4'],
    [('f',['A1', 'A4']), ('Y', ['B2', 'A4'])],
    {'A1', 'B2', 'A4'},
    Real
)

finStatesFrag3 = buildFragment(
    ['A1', 'B2'],
    [('g',['A1', 'B2'])],
    {'A1', 'B2'},
    Real
)

finStatesFGG = FGG(
    {finStatesFrag0, finStatesFrag1, finStatesFrag2, finStatesFrag3},
    {'S','X','Y'},
    'S',
    {Production('S', finStatesFrag0),
     Production('S', finStatesFrag1),
     Production('X', finStatesFrag2),
     Production('Y', finStatesFrag3)
    }
)


#-------------------------------- TESTS ----.-----------------------------------

def test_inference_finite_variables_example1():
    '''
    Testing inference in the finite variable domain case on a self constructed
    example in which case 1 of the inference algorithm applies (nonrecursive)
    '''
    fggsp = FGGsum_product(nonRecFGG)
    assert fggsp.inference()==0.25

def test_inference_finite_variables_example2():
    '''
    Testing inference in the finite variable case on a self constructed example
    in which case 1 of the inference algorithm applies (nonrecursive),
    but with different domain
    '''
    nonRecFGG.set_variable_domain('V',defaultDomain)
    nonRecFGG.set_variable_domain('EXT1',defaultDomain)
    nonRecFGG.set_variable_domain('EXT2',defaultDomain)
    fggsp = FGGsum_product(nonRecFGG)
    assert fggsp.inference()==0.875

def test_inference_finite_variables_example3():
    '''
    Testing inference in the finite variable case on a self constructed example
    in which case 2 of the inference algorithm applies (linearly recursive)
    '''
    fggsp = FGGsum_product(recFGG)
    assert fggsp.inference()==0.3333333333333333

def test_inference_finite_variables_example4():
    '''
    Testing inference in the finite variable case on a self constructed example
    in which case 3 of the inference algorithm applies (nonlinearly recursive)
    '''
    fggsp = FGGsum_product(nonlinRecFGG)
    assert fggsp.inference()==0.5

def test_inference_finite_states_example1():

    fggsp = FGGsum_product(finStatesFGG)

    finStatesDomain = VariableDomain(False)
    finStatesDomain.set_content({0, 1})
    finStatesFunction = DiscreteDensity([[0.1, 0.5],[0.3, 0.2]])

    for p in finStatesFGG.P:
        for v in p.body.V:
            v.domain = finStatesDomain
        for e in p.body.E:
            if e.label not in finStatesFGG.N:
                e.function = finStatesFunction

    fggsp.inference_finite_states()
    assert True

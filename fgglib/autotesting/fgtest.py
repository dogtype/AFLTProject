from fgglib.fg.factorgraphs import Factorgraphs

# Example 3 from Chiang, David, and Darcey, Riley. "Factor Graph Grammars." (2020).
hmmFG = Factorgraphs(
    {0,1,2,3,4,5,6,7}, # V
    {'e0','e1','e2','e3','e4','e5','e6','e7','e8'}, # E
    {'e0':{0},'e1':{0,1},'e2':{1,2},'e3':{1,3},'e4':{3,4},'e5':{3,5},
     'e6':{5,6},'e7':{5,7},'e8':{7}}, # att
    {0:'T0',1:'T1',2:'W2',3:'T3',4:'W4',5:'T5',6:'W6',7:'T7'}, # labV
    {'e0':'e0','e1':'e1','e2':'e2','e3':'e3','e4':'e4','e5':'e5','e6':'e6','e7':'e7','e8':'e8'}, # labE
    {}, # Omega (set of possible tags or words)
    {} # Phi (probability function in dependance of the adjacent variables)
)

# Figure 4.1 from Wymeersch, H. (2007). Factor graphs and the sum–product algorithm.
spaFG = Factorgraphs(
    {0,1,2,3}, # V
    {'e0','e1','e2'}, # E
    {'e0':{0},'e1':{0,1},'e2':{0,2,3}}, # att
    {0:'X1',1:'X2',2:'X3',3:'X4'}, # labV
    {'e0':'fA','e1':'fB','e2':'fC'}, # labE
    {}, # Omega (set of possible input values = real numbers?)
    {} # Phi (factorized subfunctions doing arbitrary stuff)
)

# Figure 3 from Chiang, David, and Darcey, Riley. "Factor Graph Grammars." (2020)., using only specific production rules
conFG = Factorgraphs( # not completed yet. I need to write this down first though
    {0,1,2,3,4,5,6,7}, # V
    {'e0','e1','e2','e3','e4','e5','e6','e7','e8'}, # E
    {'e0':{0},'e1':{0,1},'e2':{1,2},'e3':{1,3},'e4':{3,4},'e5':{3,5},
     'e6':{4,6},'e7':{4,7},'e8':{7}}, # att
    {0:'T0',1:'T1',2:'W2',3:'T3',4:'W4',5:'T5',6:'W6',7:'T7'}, # labV
    {}, # labE
    {}, # Omega (set of possible tags or words)
    {} # Phi (probability function in dependance of the adjacent variables)
)

def test_printout():
    print(hmmFG)
    hmmFG.draw()
    assert True

def test_sum_product():
    assert True

test_printout()

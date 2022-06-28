from fgglib.fg.factorgraph import Factorgraph

# Example 3 from Chiang, David, and Darcey, Riley. "Factor Graph Grammars." (2020).
hmmFG = Factorgraph(
    {0,1,2,3,4,5,6,7}, # V
    {'e0','e1','e2','e3','e4','e5','e6','e7','e8'}, # E
    {'e0':{0},'e1':{0,1},'e2':{1,2},'e3':{1,3},'e4':{3,4},'e5':{3,5},
     'e6':{5,6},'e7':{5,7},'e8':{7}}, # att
    {0:'T0',1:'T1',2:'W2',3:'T3',4:'W4',5:'T5',6:'W6',7:'T7'}, # labV
    {'e0':'e0','e1':'e1','e2':'e2','e3':'e3','e4':'e4','e5':'e5','e6':'e6','e7':'e7','e8':'e8'}, # labE
    {}, # Omega (set of possible tags or words)
    {} # Phi (probability function in dependance of the adjacent variables)
)

def test_print():
    print(hmmFG)
    hmmFG.draw()

test_print()

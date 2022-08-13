from fgglib.base.semiring import Tropical
from fgglib.fg.factorfunction import FactorFunction

class TropicalMul(FactorFunction):
    def __init__(self, num_arg):
        super().__init__(Tropical, num_arg)
            
    def compute(self, *args):
        if len(args) != self.arg_num:
            raise Exception("wrong number of arguments")
        
        res = Tropical.one
        for value in args:
            res *= Tropical(value)
        return res
    
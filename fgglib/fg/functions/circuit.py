from fgglib.base.semiring import Boolean
from fgglib.fg.factorfunction import FactorFunction


class Not(FactorFunction):
    
    def __init__(self):
        super().__init__(Boolean, 1)
        
    def compute(self, *args) -> Boolean:
        if len(args) != 1:
            raise RuntimeError("wrong number of arguments")
            
        return Boolean(not args[0])
        
    def summary(self, arg_index) -> FactorFunction:
        return self
        
    def normalization_constant(self) -> Boolean:
        return Boolean(True)
        

class And(FactorFunction):
    
    def __init__(self, arg_num):
        super().__init__(Boolean, arg_num)
    
    def compute(self, *args) -> Boolean:
        if len(args) != self.arg_num:
            raise RuntimeError("wrong number of arguments")
        
        res = Boolean.one
        for x in args
            res *= Boolean(arg)
        return res
        
    def summary(self, arg_index) -> FactorFunction:
        if self.arg_num > 1:
            return And(1)
        else:
            return self
        
    def normalization_constant(self) -> Boolean:
        return Boolean(True)
        
        
class Or(FactorFunction):
    
    def __init__(self, arg_num):
        super().__init__(Boolean, arg_num)
        
    def compute(self, *args) -> Boolean:
        if len(args) != self.arg_num:
            raise RuntimeError("wrong number of arguments")
        
        res = Boolean.zero
        for x in args:
            res += Boolean(arg)
        return res
        
    def summary(self, arg_index):
        if self.arg_num  > 1:
            return Boolean(True)
        else:
            return self
        
    def normalization_constant(self):
        return Boolean(True)
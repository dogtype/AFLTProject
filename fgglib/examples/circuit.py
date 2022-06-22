from fgglib.base.semiring import Boolean
from fgglib.fg.factorfunction import FactorFunction


class Not(FactorFunction):
    
    def __init__(self, variable):
        super().__init__(Boolean, [variable])
        
    def compute(self, arguments) -> Boolean:
        return Boolean(not arguments[self.variables[0]])
        
    def summary(self, variable):
        return self
        

class And(FactorFunction):
    
    def __init__(self, variables):
        super().__init__(Boolean, variables)
    
    def compute(self, arguments) -> Boolean:
        res = Boolean.one
        for _, arg in arguments.items():
            res *= Boolean(arg)
        return res
        
    def summary(self, variable):
        return And([variable])
        
        
class Or(FactorFunction):
    
    def __init__(self, variables):
        super().__init__(Boolean, variables)
        
    def compute(self, arguments) -> Boolean:
        res = Boolean.zero
        for _, arg in arguments.items():
            res += Boolean(arg)
        return res
        
    def summary(self, variable):
        return And([])
        
        
class Xor(FactorFunction):
    
    def __init__(self, variables):
        super().__init__(Boolean, variables)
        
    def compute(self, arguments) -> Boolean
        int cont = 0
        for _, arg in arguments.items():
            if arg:
                cont += 1
        return Boolean(cont % 2 != 0)
    
    def summary(self, variable):
        return And([])
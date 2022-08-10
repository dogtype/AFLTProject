from abc import *

class FactorFunction(ABC):

    def __init__(self, R, arg_num):
        self.R = R
        self.arg_num = arg_num

    def __mul__(self, other):
        return MultiplicativeFactorFunction(self, other)

    @abstractmethod
    def compute(self, *args):
        pass
    
    @abstractmethod
    def summary(self, arg_index):
        pass
    
    @abstractmethod
    def normalization_constant(self):
        pass
        

class MultiplicativeFactorFunction(FactorFunction):

    def __init__(self, factor1, factor2):
        self.factor1 = factor1
        self.factor2 = factor2
        self.arg_num = max(factor1.arg_num, factor2.arg_num)

    def compute(self, *args):
        return self.factor1.compute(args[:factor1.arg_num]) * self.factor2.compute(args[:factor2.arg_num])

    def summary(self, arg_index):
        return self.factor1.summary(arg_index) * self.factor2.summary(arg_index)
        
    def normalization_constant(self):
        return self.factor1.normalization_constant() * self.factor2.normalization_constant()
        

class IdentityFactorFunction(FactorFunction):

    def __init__(self, R):
        self.R = R
        self.arg_num = 0

    def __mul__(self, other):
        return other

    def compute(self, *args):
        return self.R.one

    def summary(self, arg_index):
        return self
        
    def normalization_constant(self):
        return self.R.one
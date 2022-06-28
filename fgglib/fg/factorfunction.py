from abc import *

class FactorFunction(ABC):

    def __init__(self, R, variables):
        self.R = R
        self.variables = variables

    def __add__(self, other):
        if self.R != other.R:
            raise ValueError
        return AdditiveFactorFunction(self, other)

    def __mul__(self, other):
        if self.R != other.R:
            raise ValueError
        return MultiplicativeFactorFunction(self, other)

    @abstractmethod
    def compute(self, arguments):
        pass

    @abstractmethod
    def summary(self, variable):
        pass


class AdditiveFactorFunction(FactorFunction):

    def __init__(self, factor1, factor2):
        self.factor1 = factor1
        self.factor2 = factor2
        self.variables = factor1.variables + [var for var in factor2.variables if var not in factor1.variables]

    def compute(self, arguments):
        arguments1 = {key:value for key, value in arguments.items() if key in self.factor1.variables}
        arguments2 = {key:value for key, value in arguments.items() if key in self.factor2.variables}
        self.factor1.compute(arguments1) + self.factor2.compute(arguments2)

    def summary(self, variable):
        return self.factor1.summary(variable) + self.factor2.summary(variable)


def MultiplicativeFactorFunction(FactorFunction):

    def __init__(self, factor1, factor2):
        self.factor1 = factor1
        self.factor2 = factor2
        self.variables = factor1.variables + [var for var in factor2.variables if var not in factor1.variables]

    def compute(self, arguments):
        arguments1 = {key:value for key, value in arguments.items() if key in self.factor1.variables}
        arguments2 = {key:value for key, value in arguments.items() if key in self.factor2.variables}
        self.factor1.compute(arguments1) * self.factor2.compute(arguments2)

    def summary(self, variable):
        return self.factor1.summary(variable) * self.factor2.summary(variable)


class IdentityFactorFunction(FactorFunction):

    def __init__(self, R):
        self.R = R
        self.variables = []

    def __mul__(self, other):
        return other

    def compute(self, arguments):
        return R.one

    def summary(self, variable):
        return self

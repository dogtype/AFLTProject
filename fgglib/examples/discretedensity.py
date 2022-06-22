from fgglib.base.semiring import Real
from fgglib.fg.factorfunction import FactorFunction

import numpy as np

class DiscreteDensity(FactorFunction):
    # for now we limit to random variable with a contingous subset {0, 1, ... X} of N  as codomain
    
    def __init__(self, variables, raw_pmf):
        if len(variables) != np.ndim(raw_pmf)
            raise ValueError("dimensions of pmf and variables number do not coincide")
        super(Real, variables)
        self.pmf = np.asarray(raw_pmf, dtype=np.float64)
        self.normalize()
        
    def __add__(self, other):
        if self.variables != other.variables:
            return super().__add__(other)
        else:
            DiscreteDensity(variables, self.pmf + other.pmf)
        
    def __mul__(self, other):
        if self.variables != other.variables:
            return super().__mul__(other)
        else
            return DiscreteDensity(variables, self.pmf * other.pmf)
        
    def compute(self, arguments):
        return self.pmf[tuple(arguments[var] for var in self.variables)]
            
    def summary(self, variable):
        new_f = DiscreteDensity([variable], np.sum(self.pmf, tuple(var for var in variables if var != variable))))
        new_f.normalize()
        return new_f
        
    def normalize(self):
        new_pmf = self.pmf / np.abs(np.sum(self.pmf))
        return DiscreteDensity(self.variables, new_pmf)
# the idea is that you can a) do whatever you want with only finite domain functions b) do a graph with one type of infinite domain and one type of functions
# one class of functions at time is our assumption!!!!! sumplify a lot the usage

from abc import *

class FactorFunction(ABC):

    def __init__(self, R, arg_num):
        self.R = R
        self.arg_num = arg_num
        
    def __add__(self, other):
        return SumFactorFunction(self, other)
        
    @abstractmethod
    def compute(self, *args):
        '''
        Computes the value the functions assumes with some specific arguments.
        Assumptions:
            - the arguments are compatible with the function
        
        Args:
            args (tuple): the arguments to evaluate the function on
            
        Returns:
            Semiring: the value of the function
        '''
        
        pass
    
    def left_mul(self, other, arg_index):
        return NaiveProductFactorFunction(self, other, arg_index)
        
    def marginal(self, arg_index, *domains):
        if len(domains) != self.arg_num:
            raise Exception("you must pass one domain for each argument of the function")
        
        arg_combs = []
        for i, d in enumerate(domains):
            if len(fixed_arg_combs) == 0:
                if i == arg_index:
                    fixed_arg_combs.append([None])
                else:
                    for value in d.enumerate():
                        fixed_arg_combs.append([value])
            else:
                new_fixed_arg_combs = []
                if i == arg_index:
                    new_fixed_arg_comba += [a + [None] for a in fixed_arg_combs]
                else:
                    for value in d.enumerate():
                        new_fixed__arg_combs += [a + [value] for a in fixed_arg_combs]
                fixed_arg_combs = new_fixed_arg_combs
            
        s = AddIdentityFactorFunction(self.R)
        for comb in fixed_arg_combs:
            s += FixedArgsFactorFunction(self, *comb)
        return s
        
            
    def normalization_constant(self, *domains):
        '''
        Computes the normalization constant Z of the FactorFunction.
        Recall that Z is the sum of the values the function assumes over all possible arguments
        assignments.
        Assumptions:
            - the domains are compatible with the functions, i.e. their content is a subset of
                the set of correct arguments implicitly defined by the function's compute method
                
        Args:
            domains (tuple[VariableDomain]): tuple containing the domain for each argument of the function
            
        Returns:
            Semiring: the normalization constant value
            
        Raises:
            Exception: if some of the domains is infinite, this naive implementation cannot compute
                the normalization constant, as it does not make any assumptions on the functions structure
        '''
        
        if len(domains) != self.arg_num:
            raise Exception("you must pass one domain for each argument of the function")
            
        arg_combs = []
        for d in domains:
            if len(arg_combs) == 0:
                for value in d.enumerate():
                    arg_combs.append([value])
            else:
                new_arg_com = []
                for value in d.enumerate():
                    new_arg_comba += [a + [value] for a in arg_combs]
                arg_combs = new_arg_combs
            
        Z = self.R.zero
        for comb in arg_combs:
            Z += self.compute(*arg_combs)


class SumFactorFunction(FactorFunction):
    def __init__(self, factor1, factor2):
        if factor1.arg_num != factor2.arg_num:
            raise Exception("sum operands must have the same arguments")
        
        self.factor1 = factor1
        self.factor2 = factor2
        self.arg_num = factor1.arg_num

    def compute(self, *args):
        return self.factor1.compute(args) + self.factor2.compute(args)

    def marginal(self, arg_index):
        return self.factor1.summary(arg_index) + self.factor2.summary(arg_index)
        
    def normalization_constant(self):
        return self.factor1.normalization_constant() + self.factor2.normalization_constant()
        

class ConstantFactorFunction(FactorFunction):
    
    def __init__(self, R, value):
        super().__init__(R, 0)
        self.value = value
        
    def compute(self, *args):
        return self.value

    def marginal(self, arg_index, *domains):
        return self
        
    def normalization_constant(self, *domains):
        return self.value
        

class AddIdentityFactorFunction(ConstantFactorFunction):
    
    def __init__(self, R):
        super().__init__(R, R.zero)
    
    def __add__(self, other):
        return other


class MulIdentityFactorFunction(ConstantFactorFunction):
    
    def __init__(self, R):
        super().__init__(R, R.zero)
    
    def left_mul(self, other, arg_index):
        return other
        
        
class FixedArgsFactorFunction(FactorFunction):
    
    def __init__(self, f, *fixed_args):
        super().__init__(f.R, fixed_args.count(None))
        self.fixed_args = fixed_args
        
    def _fill_args(self, *args):
        indexes_to_fill = [idx for idx, value in enumerate(self.fixed_args) if value is None]
        if len(indexes_to_fill) != len(args):
            raise Exception("wrong number of arguments")
            
        filled_args = [value for value in self.fixed_args]
        for i, value in enumerate(args):
            filled_args[indexes_to_fill[i]] = value
            
        return filled_args
        
    def _fill_domains(self, *domains):
        indexes_to_fill = [idx for idx, value in enumerate(self.fixed_args) if value is None]
        if len(indexes_to_fill) != len(args):
            raise Exception("wrong number of domains")
        
        filled_domains = [VariableDomain(False) if value is not None else None for value in self.fixed_args]
        for i, value in enumerate(self.fixed_args):
            if value is not None:
                fixed_domains[i].set_content({value})
        for i, d in enumerate(domains):
            filled_domains[indexes_to_fill[i]] = d
        
    def compute(self, *args):
        return self.f.compute(*(self._fill_args(*args)))
        
    def marginal(self, arg_index, *domains):
        cont = 0
        shift = 0
        for i, value in enumerate(self.fixed_args):
            if self.fixed_args[i] is None:
                if cont == arg_index:
                    for j in range(0, i):
                        if self.fixed_args[j] is not None:
                            shift += 1
                    break
                else:
                    cont += 1
        
        return self.f.summary(shift + arg_index, *(self._fill_domains(*domains)))
    
    def normalization_constant(self, *domains):
        return self.f.normalization_constant(*(self._fill_domains(*domains)))
        
        
class NaiveProductFactorFunction(FactorFunction):
    
    def __init__(self, factor1, factor2, arg2_index):
        self.factor1 = factor1
        self.factor2 = factor2
        self.arg_num = factor1.arg_num
        self.arg2_index = arg2_index

    def compute(self, *args):
        return self.factor1.compute(args) * self.factor2.compute(args[self.arg2_index])
from abc import *
from fgglib.fg.variabledomain import VariableDomain

class FactorFunction(ABC):
    '''
    Abstract class that represents a function attached to a factor in a factor graph.
    '''

    def __init__(self, R, arg_num):
        '''
        Creates a new FactorFunction object.

        Args:
            R (): Semiring class, it will be the codomain of the function.
            arg_num (int): Number of arguments the function accepts.

        Returns:
            FactorFunction: The newly created FactorFunction object.
        '''

        self.R = R
        self.arg_num = arg_num

    def __add__(self, other):
        '''
        Creates a new FactorFunction that is the result of the addition of other two functions
        that have the same arguments.

        Args:
            other (FactorFunction): The second operando of the sum.

        Returns:
            SumFactorFunction: The function representing the sum.

        Raises:
            Exception: If the operands do not have the same arguments.
        '''

        if self.arg_num != other.arg_num:
            raise Exception("sum operands must have the same arguments")

        return SumFactorFunction(self, other)

    @abstractmethod
    def compute(self, *args):
        '''
        Computes the value the functions assumes with some specific arguments.
        Assumptions:
            - the arguments are compatible with the function.

        Args:
            args (tuple): The arguments to evaluate the function on.

        Returns:
            Semiring: The value of the function.
        '''

        pass

    def left_mul(self, other, arg_index):
        '''
        It multiplies the FactorFunction by another one, used during the sum-product algorithm.
        The second operands has only one argument, shared with self.
        Assumptions:
            - the resulting function will be used only with finite variable domains, in order to
                work with infinite domains this method must be overriden.

        Args:
            other (FactorFunction): The second operand of the multiplication.
            arg_index (int): It is the index other's argument has w.r.t self arguments.

        Returns:
            NaiveProductFactorFunction: The function representing the product.

        Raises:
            Exception: If other does not have only one argument shared with self.
        '''

        if other.arg_num != 1 or arg_index >= self.arg_num:
            raise Exception("the second operand must have only one argument, shared with the first")

        return NaiveProductFactorFunction(self, other, arg_index)

    def marginal(self, arg_index, *domains):
        '''
        Marginalize the function w.r.t to one argument.
        Assumptions:
            -the domains are compatible with the functions, i.e. their content is a subset of
                the set of correct arguments implicitly defined by the function's compute method
            - all domains are finite and the resulting function will be used only with finite variable domains,
                in order to work with infinite domains this method must be overriden.

        Args:
            arg_index (int): The index of the argument we will keep "free" while marginalizing.
            domains (tuple[VariableDomain]): The domains for all the arguments of the function.

        Returns:
            FactorFunction: The marginal function.

        Raises:
            Exception: If arg_index is incorrect, the number of domains is incorrect or some domain is infinite.
        '''

        if arg_index < 0 or arg_index >= self.arg_num:
            raise Exception("incorrect arg_index parameter")

        if len(domains) != self.arg_num:
            raise Exception("you must pass one domain for each argument of the function")

        for d in domains:
            if d.infinite:
                raise Exception("to work with infinite domains, marginal method must be overridden")

        fixed_arg_combs = []
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
                    new_fixed_arg_combs += [a + [None] for a in fixed_arg_combs]
                else:
                    for value in d.enumerate():
                        new_fixed_arg_combs += [a + [value] for a in fixed_arg_combs]
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
            - all domains are finite, in order to work with infinite domains this method must be overridden.

        Args:
            domains (tuple[VariableDomain]): Tuple containing the domain for each argument of the function.

        Returns:
            Semiring: The normalization constant value.

        Raises:
            Exception: If the number of domains is incorrect or some domain is infinite.
        '''
        if len(domains) != self.arg_num:
            raise Exception("you must pass one domain for each argument of the function")

        for d in domains:
            if d.infinite:
                raise Exception("to work with infinite domains, marginal method must be overridden")

        arg_combs = []
        for d in domains:
            if len(arg_combs) == 0:
                for value in d.enumerate():
                    arg_combs.append([value])
            else:
                new_arg_combs = []
                for value in d.enumerate():
                    new_arg_combs += [a + [value] for a in arg_combs]
                arg_combs = new_arg_combs

        Z = self.R.zero
        for comb in arg_combs:
            Z += self.compute(*comb)
        return Z


class SumFactorFunction(FactorFunction):
    '''
    Class that represents the sum of two different factor functions with the same arguments.
    '''

    def __init__(self, factor1, factor2):
        '''
        Creates a new SumFactorFunction object.

        Args:
            factor1 (FactorFunction): The first sum operand.
            factor2 (FactorFunction): The second sum operand.

        Returns:
            SumFactorFunction: the result of the sum.

        Raises:
            Exception: If the two operands do not have the same number of arguments.
        '''

        if factor1.arg_num != factor2.arg_num:
            raise Exception("sum operands must have the same arguments")

        super().__init__(factor1.R, factor1.arg_num)
        self.factor1 = factor1
        self.factor2 = factor2
        self.arg_num = factor1.arg_num

    def compute(self, *args):
        '''
        See FactorFunction.compute docstring.
        '''

        return self.factor1.compute(*args) + self.factor2.compute(*args)

    def marginal(self, arg_index, *domains):
        '''
        See FactorFunction.marginal docstring.
        '''

        return self.factor1.marginal(arg_index, *domains) + self.factor2.marginal(arg_index, *domains)

    def normalization_constant(self, *domains):
        '''
        See FactorFunction.normalization_constant docstring.
        '''
        return self.factor1.normalization_constant(*domains) + self.factor2.normalization_constant(*domains)


class ConstantFactorFunction(FactorFunction):
    '''
    Class that represent a FactorFunction with zero arguments and a fixed output value.
    '''

    def __init__(self, R, value):
        '''
        Creates the new ConstantFactorFunction object.

        Args:
            R (): Semiring class, it will be the codomain of the function.
            value (Semiring): The fixed value the functions assumes.
        '''

        super().__init__(R, 0)
        self.value = value

    def compute(self, *args):
        '''
        Compute the function value, i.e. always return self.value whatever args are passed.

        Args:
            args (tuple): The arguments passed, they should be zero, but are ignored anyway.

        Returns:
            Semiring: The fixed value of the function.
        '''

        return self.value

    def marginal(self, arg_index, *domains):
        '''
        Computes the marginal. Given that a constant function has no argument, the marginal will
        be the function itself.

        Args:
            arg_index (int): The index of the "free" argument, it is ignored as the function has zero arguments
            domains (tuple[VariableDomain]): The domains of the arguments. Ignored as well.

        Returns:
            ConstantFactorFunction: The marginal, which always coincides with self.
        '''

        return self

    def normalization_constant(self, *domains):
        '''
        Computes the normalization constant Z of the FactorFunction.
        Recall that Z is the sum of the values the function assumes over all possible arguments
        assignments. In the case of a constant function, Z is equal to the constant value.

        Args:
            domains (tuple[VariableDomain]): The domains of the arguments. Ignored, given that there are zero arguments.

        Returns:
            Semiring: The value of Z, which always coincides with self.value.
        '''
        return self.value


class AddIdentityFactorFunction(ConstantFactorFunction):
    '''
    Class that represent a constant function with the additive identity as the fixed value.
    '''

    def __init__(self, R):
        '''
        Creates the new AddIdentityFactorFunction object.

        Args:
            R (): Semiring whose additive identity will be the value.

        Returns.
            AddIdentityFactorFunction: The newly created object.
        '''

        super().__init__(R, R.zero)

    def __add__(self, other):
        '''
        Add together self and another factor function. Given that self is the additive identity,
        it always return the other function.

        Args:
            other (FactorFunction): The second operand of the sum.

        Returns.
            FactorFunction: The result of the sum, always coincides with other.
        '''

        return other


class MulIdentityFactorFunction(ConstantFactorFunction):
    '''
    Class that represent a constant function with the multiplicative identity as the fixed value.
    '''

    def __init__(self, R):
        '''
        Creates the new MulIdentityFactorFunction object.

        Args:
            R (): Semiring whose multiplicative identity will be the value.

        Returns.
            MulIdentityFactorFunction: The newly created object.
        '''

        super().__init__(R, R.one)

    def left_mul(self, other, arg_index):
        '''
        It multiplies the FactorFunction by another one, used during the sum-product algorithm.
        Given that the first operand is the multiplicative identity, the operation is valid even if
        the second operands does not have only one argument, shared with self.

        Args:
            other (FactorFunction): The second operand of the multiplication.
            arg_index (int): It is the index other's argument has w.r.t self arguments.

        Returns:
            FactorFunction: The function representing the product, always coincides with other.
        '''

        return other


class FixedArgsFactorFunction(FactorFunction):
    '''
    Class that represents a function with some argument that have a predefined fixed value,
    while others are free. The actual arguments of the function are the free ones.
    '''

    def __init__(self, f, *fixed_args):
        '''
        Created a new FixedArgsFactorFunction object.

        Args:
            f (FactorFunction): The original function.
            fixed_args (tuple): Tuple with one value for each argument. The free arguments have a None.

        Returns:
            FixedArgsFactorFunction: The newly created object.

        Raises:
            Exception: If fixed_args has an incorrect length.
        '''

        if len(fixed_args) != f.arg_num:
            raise Exception("wrong number of fixed arguments")

        super().__init__(f.R, fixed_args.count(None))
        self.f = f
        self.fixed_args = fixed_args

    def _fill_args(self, *args):
        '''
        Given the arguments to the FixedArgsFactorFunction, it fill a list with the corresponding arguments
        to pass to the original function.

        Args:
            args (tuple): the value we want to pass to the free arguments of this function

        Returns:
            list: List containing the fixed arguments and the one in args, ready to be passed to the original
                function's compute method.

        Raises:
            Exception: If args has an incorrect size.
        '''

        indexes_to_fill = [i for i, value in enumerate(self.fixed_args) if value is None]
        if len(indexes_to_fill) != len(args):
            raise Exception("wrong number of arguments")

        filled_args = [value for value in self.fixed_args]
        for i, value in enumerate(args):
            filled_args[indexes_to_fill[i]] = value

        return filled_args

    def _fill_domains(self, *domains):
        '''
        Given the domains to the FixedArgsFactorFunction, it fill a list with the corresponding domains
        to pass to the original function.

        Args:
            domains (tuple[VariableDomain]): the domains we want to pass to the free arguments of this function

        Returns:
            list[VariableDomain]: List containing the fixed domains and the ones in the argument of this method.

        Raises:
            Exception: If domains has an incorrect size.
        '''

        indexes_to_fill = [i for i, value in enumerate(self.fixed_args) if value is None]
        if len(indexes_to_fill) != len(domains):
            raise Exception("wrong number of domains")

        filled_domains = [VariableDomain(False) if value is not None else None for value in self.fixed_args]
        for i, value in enumerate(self.fixed_args):
            if value is not None:
                filled_domains[i].set_content({value})
        for i, d in enumerate(domains):
            filled_domains[indexes_to_fill[i]] = d

        return filled_domains

    def compute(self, *args):
        '''
        See FactorFunction.compute docstring.
        '''
        return self.f.compute(*(self._fill_args(*args)))

    def marginal(self, arg_index, *domains):
        '''
        Marginalize the function w.r.t to one argument. In order to do it, it computes the shift to apply
        to arg_index and then call the marginal method of the original functions.
        Assumptions:
            -the domains are compatible with the functions, i.e. their content is a subset of
                the set of correct arguments implicitly defined by the function's compute method

        Args:
            arg_index (int): The index of the argument we will keep "free" while marginalizing.
            domains (tuple[VariableDomain]): The domains for all the arguments of the function.

        Returns:
            FactorFunction: The marginal function.

        Raises:
            Exception: If arg_index is incorrect, the number of domains is incorrect or some domain is infinite.
        '''
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

        return self.f.marginal(shift + arg_index, *(self._fill_domains(*domains)))

    def normalization_constant(self, *domains):
        '''
        Computes the normalization constant Z of the FixedArgsFactorFunction.
        Recall that Z is the sum of the values the function assumes over all possible arguments
        assignments. In order to do it, it add do the proper domains a dummy single-valued domain
        for each of the fixed arguments.
        Assumptions:
            - the domains are compatible with the functions, i.e. their content is a subset of
                the set of correct arguments implicitly defined by the function's compute method

        Args:
            domains (tuple[VariableDomain]): Tuple containing the domain for each (free) argument of the function.

        Returns:
            Semiring: The normalization constant value.
        '''
        return self.f.normalization_constant(*(self._fill_domains(*domains)))


class NaiveProductFactorFunction(FactorFunction):
    '''
    Class that represents the result of the multiplication bewteen two factor functions, with second one
    that only has one argument, shared with the first. This can be used only if the resulting function
    will work exclusively with finite domains. In order to work with infinite domains, FactorFunction.left_mul
    must be overridden, thus this class would not be used anymore.
    '''

    def __init__(self, factor1, factor2, arg2_index):
        '''
        Creates a new NaiveProductFactorFunction object.

        Args:
            factor1 (FactorFunction): The first operand of the product.
            factor2 (FactorFunction): The second operand of the product.
            arg2_index (int) : It is the index factor2's argument has w.r.t factor2 arguments.

        Returns:
            NaiveProductFactorFunction: The function representing the product.

        Raises:
            Exception: If factor2 does not have only one argument shared with factor1.
        '''

        if factor2.arg_num != 1 or arg2_index >= factor1.arg_num:
            raise Exception("the second operand must have only one argument, shared with the first")

        super().__init__(factor1.R, factor1.arg_num)
        self.factor1 = factor1
        self.factor2 = factor2
        self.arg2_index = arg2_index

    def compute(self, *args):
        '''
        See FactorFunction.compute docstring.
        '''
        return self.factor1.compute(*args) * self.factor2.compute(args[self.arg2_index])

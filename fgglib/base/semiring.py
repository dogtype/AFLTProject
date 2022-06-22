# from https://github.com/rycolab/aflt-f2022/blob/main/rayuela/base/semiring.py

import numpy as np
from fractions import Fraction

from collections import defaultdict


class Semiring:

    zero = None
    one = None
    idempotent = False

    def __init__(self, score):
        self.score = score

    @classmethod
    def zeros(cls, N, M):
        return np.full((N, M), cls.zero)

    @classmethod
    def chart(cls, default=None):
        if default is None:
            default = cls.zero
        return dd(lambda : default)

    @classmethod
    def diag(cls, N):
        W = cls.zeros(N, N)
        for n in range(N):
            W[n, n] = cls.one

        return W

    def __add__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        return self.score == other.score

    def __hash__(self):
        return hash(self.score)
        
        
class Boolean(Semiring):

    def __init__(self, score):
        super().__init__(score)

    def star(self):
        return Boolean.one

    def __add__(self, other):
        return Boolean(self.score or other.score)

    def __mul__(self, other):
        if other.score is self.one: return self.score
        if self.score is self.one: return other.score
        if other.score is self.zero: return self.zero
        if self.score is self.zero: return self.zero
        return Boolean(other.score and self.score)

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f'{self.score}'

    def __str__(self):
        return str(self.score)

    def __hash__(self):
        return hash(self.score)

Boolean.zero = Boolean(False)
Boolean.one = Boolean(True)
Boolean.idempotent = True


class Real(Semiring):

    def __init__(self, score):
        # TODO: this is hack to deal with the fact
        # that we have to hash weights
        self.score = score

    def star(self):
        return Real(1.0/(1.0-self.score))

    def __float__(self):
        return float(self.score)

    def __add__(self, other):
        return Real(self.score +  other.score)

    def __mul__(self, other):
        if other is self.one: return self
        if self is self.one: return other
        if other is self.zero: return self.zero
        if self is self.zero: return self.zero
        return Real(self.score * other.score)

    def __invert__(self):
        return Real(1.0/self.score)

    def __truediv__(self, other):
        return Real(self.score / other.score)

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        #return f'Real({self.score})'
        return f'{round(self.score, 15)}'

    def __eq__(self, other):
        #return float(self.score) == float(other.score)
        return np.allclose(float(self.score), float(other.score), atol=1e-3)

    # TODO: find out why this wasn't inherited
    def __hash__(self):
        return hash(self.score)

Real.zero = Real(0.0)
Real.one = Real(1.0)
Real.idempotent = False
Real.cancellative = True
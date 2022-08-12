from fgglib.base.semiring import Real
from fgglib.fg.factorfunction import FactorFunction

import numpy as np

class NormalDensity(FactorFunction):

    def __init__(self, cap_lambda, eta, scale_factor=1):
        super().__init__(Real, cap_lambda.shape[0])
        self.cap_lambda = cap_lambda
        self.eta = eta
        self.scale_factor = scale_factor
        
    @classmethod
    def from_moments(cls, mean, cov, scale_factor = 1):
        cap_lambda = np.linalg.inv(np.asarray(cov, dtype=np.float64))
        eta = np.dot(cap_lambda, np.asarray(mean, dtype=np.float64))
        return cls(cap_lambda, eta, scale_factor)
        
    def get_mean(self):
        return np.dot(np.linalg.inv(self.cap_lambda), self.eta)
        
    def get_cov(self):
        return np.linalg.inv(self.cap_lambda)
    
    def _get_xi(self):
        return -0.5 * (self.cap_lambda.shape[0] * np.log(2 * numpy.pi) - np.log(np.linalg.det(self.cap_lambda)) + np.dot(np.dot(np.transponse(self.eta), np.linalg.inv(self.cap_lambda)), self.eta)
        
    def normalize(self):
        self.scale_factor = 1
    
    def compute(self, *args) -> Real:
        x = np.transpose(np.asarray(args))
        return Real(self.scale_factor * (np.exp(self._get_xi() + np.dot(np.transpose(self.eta), x)) - 0.5 * np.dot(np.dot(np.transpose(x), self.cap_lambda), x)))
    
    def left_mul(self, other, arg_index):
        new_cap_lambda = self.cap_lambda
        new_cap_lambda[arg_index][arg_index] += other.cap_lambda[0][0]
        new_eta = self.eta
        new_eta[arg_index] += other.eta[0]
        
        new_density = NormalDensity(new_cap_lambda, new_eta)
        new_density.scale_factor = self._get_xi() + other._get_xi() - new_density._get_xi()
        return new_density
        
    def marginal(self, arg_index, *domains) -> FactorFunction:
        return NormalDensity.from_moments(self.get_mean()[arg_index], self.get_cov()[arg_index][arg_index], self.scale_factor)
        
    def normalization_constant(self, *domains) -> Real:
        return Real(self.scale_factor)
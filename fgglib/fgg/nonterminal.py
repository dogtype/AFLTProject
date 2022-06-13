""" DISCLAIMER: taken from rayuela library """

from fgglib.fgg.symbol import Sym

class NT:

	def __init__(self, X, label=None, n=None):
		self._X = X
		self._label = label
		self.num = n

	@property
	def X(self):
		return self._X

	@property
	def label(self):
		return self._label

	def number(self):
		return

	def set_label(self, label):
		self._label = label

	def copy(self):
		return NT(self.X)

	def __truediv__(self, Y):
		return Slash(self, Y)

	def __invert__(self):
		return Other(self)

	def __repr__(self):
		if self.label is not None:
			return f'{self.label}'
		return f'{self.X}'

	def __hash__(self):
		return hash(self.X)

	def __eq__(self, other):
		return isinstance(other, NT) and self.X == other.X

S = NT("S")
bottom = NT("⊥")

""" DISCLAIMER: inspired by rayuela library """

from collections import namedtuple

class Production(namedtuple("Production", "head, body")):

	def __str__(self):
		return str(self.head) + " → " +  str(self.body) # requires a string representation of the factor graph fragment

	def conjoinable(self, p) -> bool:
		""" asserts if two Productions are conjoinable """
		raise NotImplementedError

	def conjoin(self, p):
		""" returns the conjunction of two different productions """
		raise NotImplementedError

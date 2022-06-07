""" DISCLAIMER: taken from rayuela library """

from collections import namedtuple

class Production(namedtuple("Production", "head, body")):

	def __str__(self):
		return str(self.head) + " → " +  str(self.body) # requires a string representation of the factor graph fragment

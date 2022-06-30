from collections import namedtuple
from fgglib.fg.fragment import Fragment

class Production(namedtuple("Production", "head, body")):

	def __str__(self):
		return str(self.head) + " → " +  str(self.body) # requires a string representation of the factor graph fragment

	def edge_in_set(self,query):
		""" checks if an edge is in the edgeset of the body, without checking label """
		edges = {(e.content, e.targets) for e in self.body.E}
		return (query.content, query.targets) in edges

	def conjoinable(self, other, nts) -> bool:
		""" asserts if two Productions are conjoinable (given a set of nonterminals) """
		if(type(self.head) != type(other.head)
		or self.body.V != other.body.V
		or self.body.external != other.body.external):
			return False
		for e in self.body.E:
			if(e.label in nts and other.edge_in_set(e)):
				return False
		for e in other.body.E:
			if(e.label in nts and other.edge_in_set(e)): # the whole nonterminal edge has to be the same? label type is also the same?
				return False

		return True
		

	def conjoin(self, other, nts):
		""" returns the conjunction of two different productions """
		new_head = (self.body.head, other.body.head)

		new_E=set()
		for e in self.body.E:
			edgeNTMap = {}
			if(e.label in nts): # case E_N
				edgeNTMap[e]=e.label
			else: # case E_1
				new_E.add(e) # careful with distinct premise
		for e in other.body.E:
			if(e.label in nts): # case E_N
				ep = Edge(e.content,(edgeNTMap[e],e.label),e.targets)
				new_E.add(ep)
			else: # case E_1
				new_E.add(e) # careful with distinct premise

		new_body = Fragment(self.body.V,new_E,self.body.external)
		return (new_head, new_body)

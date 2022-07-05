from collections import namedtuple
from fgglib.fg.edge import Edge
from fgglib.fg.fragment import Fragment

class Production(namedtuple("Production", "head, body")):

	def __str__(self):
		return str(self.head) + " → " +  str(self.body) # requires a string representation of the factor graph fragment

	def edge_in_set(self,query):
		""" checks if an edge is in the edgeset of the body, without checking label """
		for e in self.body.E:
			if(e.content==query.content and e.targets == query.targets):
				return True
		return False

	def conjoinable(self, other, nts) -> bool:
		""" asserts if two Productions are conjoinable (given a set of nonterminals) """
		if(type(self.head) != type(other.head)
		or self.body.V != other.body.V
		or self.body.external != other.body.external):
			return False
		for e in self.body.E:
			if(e.label in nts and not other.edge_in_set(e)):
				return False
		for e in other.body.E:
			if(e.label in nts and not self.edge_in_set(e)):
				return False

		# have not checked for label type! Do I?
		return True


	def conjoin(self, other, nts):
		""" returns the conjunction of two different productions """
		new_head = (self.head, other.head)

		new_E=set()
		edgeNTMap = {}
		for e in self.body.E:
			if(e.label in nts): # case E_N
				edgeNTMap[str(e.targets)]=e.label
			else: # case E_1
				new_E.add(e) # careful with distinct premise
		for e in other.body.E:
			if(e.label in nts): # case E_N
				ep = Edge(e.content,(edgeNTMap[str(e.targets)],e.label))
				for t in e.targets:
					ep.add_target(t)
				new_E.add(ep)
			else: # case E_2
				new_E.add(e) # careful with distinct premise

		new_body = Fragment()
		for v in self.body.V:
			new_body.add_vertex(v)
		for e in new_E:
			new_body.add_edge(e)
		for ext in self.body.external:
			new_body.add_external(ext)
		return Production(new_head, new_body)

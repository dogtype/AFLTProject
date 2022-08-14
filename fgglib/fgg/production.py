from collections import namedtuple
from fgglib.fg.edge import Edge
from fgglib.fg.fragment import Fragment

class Production(namedtuple("Production", "head, body")):
	'''
	A  class representing a production of a factor graph grammar. Productions are
	tuples of a head (nonterminal) and body (factor graph fragment)
	'''

	def __str__(self):
		'''
		Computes a string representation of the Production

		Returns:
			Concatenated string representation of head and body
		'''
		return str(self.head) + " → " +  str(self.body) # requires a string representation of the factor graph fragment

	def edge_in_set(self,query):
		'''
		Checks if an edge is in the edgeset of the body, without checking label

		Args:
			query (Edge): Edge to be searched in the graph fragment

		Returns:
		 	A boolean flag corrensponding to the result of the check
		'''
		for e in self.body.E:
			if(e.content==query.content and e.targets == query.targets):
				return True
		return False

	def conjoinable(self, other, nts) -> bool:
		'''
		Asserts if two Productions are conjoinable (given a set of nonterminals)

		Args:
			other (Production): The second Production to be used for the check
			nts (list): A list of labels considered nonterminals in the grammar

		Returns:
		 	A boolean flag corresponding to the result of the check
		'''
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
		'''
		Returns the conjunction of two different productions

		Args:
			other: the production rule with witch the object is to be conjoined
			nts: A list of labels that are considered to be nonterminals in the grammar

		Returns:
			Production: A new production corresponding to the conjunction of the two productions
		'''
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

		new_body = Fragment(self.body.R)
		for v in self.body.V:
			new_body.add_vertex(v)
		for e in new_E:
			new_body.add_edge(e)
		for ext in self.body.external:
			new_body.add_external(ext)
		return Production(new_head, new_body)

import canopenx
import unittest

from canopenx.node import Node
from canopenx.objectdictionary.datatypes import UNSIGNED32
from canopenx.objectdictionary.deftype import DefType
from canopenx.objectdictionary.domain import Domain
from canopenx.objectdictionary.variable import Variable


class ItemProxyTestCase(unittest.TestCase):
	def test_access(self):
		dictionary = canopenx.ObjectDictionary()

		node = Node(1, dictionary)

		# DefType
		dictionary.add(DefType("deftype", 0x3000))

		self.assertEqual(dictionary["deftype"].access_type, node["deftype"].access_type)
		self.assertEqual(dictionary["deftype"].data_type, node["deftype"].data_type)
		self.assertEqual(dictionary["deftype"].index, node["deftype"].index)
		self.assertEqual(dictionary["deftype"].name, node["deftype"].name)
		self.assertEqual(dictionary["deftype"].subindex, node["deftype"].subindex)

		# Domain
		dictionary.add(Domain("domain", 0x4000))

		self.assertEqual(dictionary["domain"].access_type, node["domain"].access_type)
		self.assertEqual(dictionary["domain"].data_type, node["domain"].data_type)
		self.assertEqual(dictionary["domain"].index, node["domain"].index)
		self.assertEqual(dictionary["domain"].name, node["domain"].name)
		self.assertEqual(dictionary["domain"].subindex, node["domain"].subindex)

		# Variable
		dictionary.add(Variable("variable", 0x6000, 0x00, UNSIGNED32))

		self.assertEqual(dictionary["variable"].access_type, node["variable"].access_type)
		self.assertEqual(dictionary["variable"].data_type, node["variable"].data_type)
		self.assertEqual(dictionary["variable"].index, node["variable"].index)
		self.assertEqual(dictionary["variable"].name, node["variable"].name)
		self.assertEqual(dictionary["variable"].subindex, node["variable"].subindex)

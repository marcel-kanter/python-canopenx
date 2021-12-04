import unittest
import canopenx

from canopenx.node import Node
from canopenx.objectdictionary import Array, DefStruct, DefType, Domain, Record, Variable
from canopenx.objectdictionary.datatypes import UNSIGNED8, UNSIGNED32


class NodeTestCase(unittest.TestCase):
	def test_init(self):
		dictionary = canopenx.ObjectDictionary()

		node_id = 0
		with self.assertRaises(ValueError):
			Node(node_id, dictionary)

		node_id = 128
		with self.assertRaises(ValueError):
			Node(node_id, dictionary)

		node_id = 1
		node = Node(node_id, dictionary)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.name, None)

		node_id = 10
		node_name = "XYZ"
		node = Node(node_id, dictionary, node_name)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.name, node_name)

	def test_equals(self):
		dictionary1 = canopenx.ObjectDictionary()
		dictionary2 = canopenx.ObjectDictionary()

		a = Node(1, dictionary1)
		b = Node(1, dictionary1)
		self.assertEqual(a, b)

		a = Node(1, dictionary1)
		b = Node(11, dictionary1)
		self.assertNotEqual(a, b)

		a = Node(1, dictionary1)
		b = Node(1, dictionary1, "B")
		self.assertNotEqual(a, b)

		a = Node(1, dictionary1)
		b = Node(1, dictionary2)
		self.assertEqual(a, b)

		dictionary2.add(Variable("variable", 0x100, 0x00, UNSIGNED8))

		a = Node(1, dictionary1)
		b = Node(1, dictionary2)
		self.assertNotEqual(a, b)

	def test_objectdictionary_proxies(self):
		dictionary = canopenx.ObjectDictionary()

		examinee = Node(1, dictionary)

		# Array
		with self.assertRaises(KeyError):
			arr = examinee["array"]

		dictionary.add(Array("array", 0x1000, UNSIGNED32))

		arr = examinee["array"]

		# DefStruct
		with self.assertRaises(KeyError):
			defstr = examinee["defstruct"]

		dictionary.add(DefStruct("defstruct", 0x2000))

		defstr = examinee["defstruct"]

		# DefType
		with self.assertRaises(KeyError):
			deftyp = examinee["deftype"]

		dictionary.add(DefType("deftype", 0x3000))

		deftyp = examinee["deftype"]

		# Domain
		with self.assertRaises(KeyError):
			dom = examinee["domain"]

		dictionary.add(Domain("domain", 0x4000))

		dom = examinee["domain"]

		# Record
		with self.assertRaises(KeyError):
			rec = examinee["record"]

		dictionary.add(Record("record", 0x5000))

		rec = examinee["record"]

		# Variable
		with self.assertRaises(KeyError):
			var = examinee["variable"]

		dictionary.add(Variable("variable", 0x6000, 0x00, UNSIGNED32))

		var = examinee["variable"]

import unittest
import canopenx

from canopenx.node import Node
from canopenx.objectdictionary import Variable
from canopenx.objectdictionary.datatypes import UNSIGNED8


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

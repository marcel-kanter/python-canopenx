import unittest

from canopenx.node import Node


class NodeTestCase(unittest.TestCase):
	def test_init(self):
		node_id = 0
		with self.assertRaises(ValueError):
			Node(node_id)

		node_id = 128
		with self.assertRaises(ValueError):
			Node(node_id)

		node_id = 1
		node = Node(node_id)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.name, None)

		node_id = 10
		node_name = "XYZ"
		node = Node(node_id, node_name)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.name, node_name)

	def test_equals(self):
		a = Node(1)
		b = Node(1)
		self.assertEqual(a, b)

		a = Node(1)
		b = Node(11)
		self.assertNotEqual(a, b)

		a = Node(1)
		b = Node(1, "B")
		self.assertNotEqual(a, b)

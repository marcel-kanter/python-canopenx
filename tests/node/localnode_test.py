import unittest

from canopenx import ObjectDictionary
from canopenx.nmt.states import INITIALIZING, OPERATIONAL
from canopenx.node import LocalNode


class LocalNodeTestCase(unittest.TestCase):
	def test_init(self):
		dictionary = ObjectDictionary()
		node_id = 1
		node = LocalNode(node_id, dictionary)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.dictionary, dictionary)

	def test_nmt(self):
		dictionary = ObjectDictionary()
		node = LocalNode(100, dictionary)

		self.assertEqual(node.nmt.state, INITIALIZING)

		node.nmt.state = OPERATIONAL
		self.assertEqual(node.nmt.state, OPERATIONAL)

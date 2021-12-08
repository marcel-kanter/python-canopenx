import unittest

from canopenx import ObjectDictionary
from canopenx.nmt.states import INITIALIZING
from canopenx.node import RemoteNode


class RemoteNodeTestCase(unittest.TestCase):
	def test_init(self):
		dictionary = ObjectDictionary()
		node_id = 1
		node = RemoteNode(node_id, dictionary)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.dictionary, dictionary)


	def test_nmt(self):
		dictionary = ObjectDictionary()
		node = RemoteNode(100, dictionary)

		self.assertEqual(node.nmt.state, INITIALIZING)

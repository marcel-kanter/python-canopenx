import unittest

from canopenx import ObjectDictionary
from canopenx.node import RemoteNode


class RemoteNodeTestCase(unittest.TestCase):
	def test_init(self):
		dictionary = ObjectDictionary()
		node_id = 1
		node = RemoteNode(node_id, dictionary)
		self.assertEqual(node.id, node_id)
		self.assertEqual(node.dictionary, dictionary)

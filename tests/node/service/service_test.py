import unittest

from canopenx import ObjectDictionary
from canopenx.node import Node
from canopenx.node.service import Service


class ServiceTestCase(unittest.TestCase):
	def test_attach(self):
		dictionary = ObjectDictionary()
		node = Node(1, dictionary)

		examinee = Service()
		self.assertFalse(examinee.is_attached())
		self.assertEqual(examinee.node, None)

		examinee.attach(node)
		self.assertTrue(examinee.is_attached())
		self.assertEqual(examinee.node, node)

		examinee.detach()
		self.assertFalse(examinee.is_attached())
		self.assertEqual(examinee.node, None)

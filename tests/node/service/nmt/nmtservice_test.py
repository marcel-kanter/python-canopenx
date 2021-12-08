import unittest

from canopenx.nmt.states import INITIALIZING
from canopenx.node.service.nmt import NMTService


class NMTServiceTestCase(unittest.TestCase):
	def test_properties(self):
		examinee = NMTService()

		self.assertEqual(examinee.state, INITIALIZING)

		with self.assertRaises(AttributeError):
			examinee.state = INITIALIZING

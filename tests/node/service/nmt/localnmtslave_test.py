import unittest

from canopenx.nmt.states import INITIALIZING, OPERATIONAL, PRE_OPERATIONAL, STOPPED
from canopenx.node.service.nmt import LocalNMTSlave


class LocalNMTSlaveTestCase(unittest.TestCase):
	def test_properties(self):
		examinee = LocalNMTSlave()

		self.assertEqual(examinee.state, INITIALIZING)

		with self.assertRaises(ValueError):
			examinee.state = -1

		with self.assertRaises(ValueError):
			examinee.state = 128

		examinee.state = PRE_OPERATIONAL
		self.assertEqual(examinee.state, PRE_OPERATIONAL)

		examinee.state = OPERATIONAL
		self.assertEqual(examinee.state, OPERATIONAL)

		examinee.state = STOPPED
		self.assertEqual(examinee.state, STOPPED)

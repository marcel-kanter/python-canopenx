import can
import canopenx
import unittest



class NetworkTestCase(unittest.TestCase):
	def test_connect(self):
		bus = can.Bus(bustype = "virtual", channel = 0)
		network = canopenx.Network()

		self.assertFalse(network.is_connected())

		network.connect(bus)
		self.assertTrue(network.is_connected())
		self.assertIs(network.bus, bus)

		network.connect(bus)
		self.assertTrue(network.is_connected())
		self.assertIs(network.bus, bus)

		network.disconnect()
		self.assertFalse(network.is_connected())
		self.assertIsNone(network.bus)

		bus.shutdown()

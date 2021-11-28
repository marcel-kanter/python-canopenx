import can
import canopenx
import mock
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

	def test_subscribe(self):
		network = canopenx.Network()
		callback1 = mock.Mock()
		callback2 = mock.Mock()

		self.assertFalse(network.subscribed(0x100, callback1))
		self.assertFalse(network.subscribed(0x100, callback2))

		with self.assertRaises(ValueError):
			network.unsubscribe(0x100, callback1)

		network.subscribe(0x100, callback1)
		self.assertTrue(network.subscribed(0x100, callback1))
		self.assertFalse(network.subscribed(0x100, callback2))

		network.subscribe(0x100, callback2)
		self.assertTrue(network.subscribed(0x100, callback1))
		self.assertTrue(network.subscribed(0x100, callback2))

		with self.assertRaises(ValueError):
			network.subscribe(0x100, callback1)
		self.assertTrue(network.subscribed(0x100, callback1))

		network.subscribe(0x200, callback1)
		self.assertTrue(network.subscribed(0x200, callback1))

		with self.assertRaises(ValueError):
			network.subscribe(0x200, callback1)
		self.assertTrue(network.subscribed(0x200, callback1))

		network.unsubscribe(0x100, callback1)
		self.assertFalse(network.subscribed(0x100, callback1))
		self.assertTrue(network.subscribed(0x100, callback2))
		self.assertTrue(network.subscribed(0x200, callback1))

		with self.assertRaises(ValueError):
			network.unsubscribe(0x100, callback1)
		self.assertFalse(network.subscribed(0x100, callback1))
		self.assertTrue(network.subscribed(0x100, callback2))
		self.assertTrue(network.subscribed(0x200, callback1))

		network.unsubscribe(0x100, callback2)
		self.assertFalse(network.subscribed(0x100, callback1))
		self.assertFalse(network.subscribed(0x100, callback2))
		self.assertTrue(network.subscribed(0x200, callback1))

		with self.assertRaises(ValueError):
			network.unsubscribe(0x100, callback2)
		self.assertFalse(network.subscribed(0x100, callback1))
		self.assertFalse(network.subscribed(0x100, callback2))
		self.assertTrue(network.subscribed(0x200, callback1))

		network.unsubscribe(0x200, callback1)
		self.assertFalse(network.subscribed(0x100, callback1))
		self.assertFalse(network.subscribed(0x100, callback2))
		self.assertFalse(network.subscribed(0x200, callback1))

import can
import canopenx
import mock
import time
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

	def test_message_passing(self):
		bus1 = can.Bus(bustype = "virtual", channel = 0)
		bus2 = can.Bus(bustype = "virtual", channel = 0)

		cb1 = mock.Mock()
		cb2 = mock.Mock()

		network = canopenx.Network()

		network.subscribe(0x100, cb1)
		network.subscribe(0x200, cb1)

		network.connect(bus1)

		# Subscription is possible before and after connect and for many callbacks
		network.subscribe(0x200, cb2)

		cb1.reset_mock()
		cb2.reset_mock()
		message = can.Message(arbitration_id = 0x100, is_extended_id = False, data = b"\x01")
		bus2.send(message, timeout = 1.0)
		time.sleep(0.1)
		cb1.assert_called_once()
		cb2.assert_not_called()

		# Comparing the message from the callback and the sent message directly is not possible - the timestamp changes
		cb_message = cb1.call_args_list[0].args[0]
		self.assertEqual(message.arbitration_id, cb_message.arbitration_id)
		self.assertEqual(message.is_extended_id, cb_message.is_extended_id)
		self.assertEqual(message.is_remote_frame, cb_message.is_remote_frame)
		self.assertEqual(message.data, cb_message.data)

		cb1.reset_mock()
		cb2.reset_mock()
		message = can.Message(arbitration_id = 0x200, is_extended_id = False, data = b"\x02")
		bus2.send(message, timeout = 1.0)
		time.sleep(0.1)
		cb1.assert_called_once()
		cb2.assert_called_once()

		# Comparing the message from the callback and the sent message directly is not possible - the timestamp changes
		cb_message = cb1.call_args_list[0].args[0]
		self.assertEqual(message.arbitration_id, cb_message.arbitration_id)
		self.assertEqual(message.is_extended_id, cb_message.is_extended_id)
		self.assertEqual(message.is_remote_frame, cb_message.is_remote_frame)
		self.assertEqual(message.data, cb_message.data)
		cb_message = cb2.call_args_list[0].args[0]
		self.assertEqual(message.arbitration_id, cb_message.arbitration_id)
		self.assertEqual(message.is_extended_id, cb_message.is_extended_id)
		self.assertEqual(message.is_remote_frame, cb_message.is_remote_frame)
		self.assertEqual(message.data, cb_message.data)

		network.unsubscribe(0x200, cb1)

		cb1.reset_mock()
		cb2.reset_mock()
		message = can.Message(arbitration_id = 0x100, is_extended_id = False, data = b"\x03")
		bus2.send(message, timeout = 1.0)
		time.sleep(0.1)
		cb1.assert_called_once()
		cb2.assert_not_called()

		# Comparing the message from the callback and the sent message directly is not possible - the timestamp changes
		cb_message = cb1.call_args_list[0].args[0]
		self.assertEqual(message.arbitration_id, cb_message.arbitration_id)
		self.assertEqual(message.is_extended_id, cb_message.is_extended_id)
		self.assertEqual(message.is_remote_frame, cb_message.is_remote_frame)
		self.assertEqual(message.data, cb_message.data)

		cb1.reset_mock()
		cb2.reset_mock()
		message = can.Message(arbitration_id = 0x200, is_extended_id = False, data = b"\x04")
		bus2.send(message, timeout = 1.0)
		time.sleep(0.1)
		cb1.assert_not_called()
		cb2.assert_called_once()

		# Comparing the message from the callback and the sent message directly is not possible - the timestamp changes
		cb_message = cb2.call_args_list[0].args[0]
		self.assertEqual(message.arbitration_id, cb_message.arbitration_id)
		self.assertEqual(message.is_extended_id, cb_message.is_extended_id)
		self.assertEqual(message.is_remote_frame, cb_message.is_remote_frame)
		self.assertEqual(message.data, cb_message.data)

		network.disconnect()

		cb1.reset_mock()
		cb2.reset_mock()
		message = can.Message(arbitration_id = 0x100, is_extended_id = False, data = b"\x05")
		bus2.send(message, timeout = 1.0)
		time.sleep(0.1)
		cb1.assert_not_called()
		cb2.assert_not_called()

		bus1.shutdown()
		bus2.shutdown()

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

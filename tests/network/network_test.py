import can
import canopenx
import mock
import time
import unittest

from canopenx.node import Node


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

	def test_collection(self):
		network = canopenx.Network()

		# Node without name
		node1 = Node(1)

		self.assertEqual(len(network), 0)
		self.assertFalse(node1.id in network)

		network.add(node1)
		self.assertEqual(len(network), 1)
		self.assertIs(network[1], node1)

		node2 = Node(2)

		network.add(node2)
		self.assertEqual(len(network), 2)
		self.assertIs(network[2], node2)

		node3 = Node(3, "C")

		network.add(node3)
		self.assertEqual(len(network), 3)
		self.assertIs(network[3], node3)
		self.assertIs(network["C"], node3)

		# Test the iterator - it shall iter over all nodes
		count = 0
		for node in network:
			self.assertTrue(node.id in network)
			count += 1
		self.assertEqual(count, len(network))

		with self.assertRaises(KeyError):
			del network[node1.name]

		del network[node1.id]
		self.assertEqual(len(network), 2)
		self.assertFalse(node1.id in network)

		del network[node2.id]
		self.assertEqual(len(network), 1)
		self.assertFalse(node2.id in network)

		del network[node3.name]
		self.assertEqual(len(network), 0)
		self.assertFalse(node3.id in network)
		self.assertFalse(node3.name in network)

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

	def test_send(self):
		bus1 = can.Bus(bustype = "virtual", channel = 0)
		bus2 = can.Bus(bustype = "virtual", channel = 0)

		network = canopenx.Network()

		#### Test step: Send on detached bus
		with self.assertRaises(RuntimeError):
			network.send(can.Message(arbitration_id = 0x00, dlc = 0))

		#### Test step: Send message and receive on other bus
		network.connect(bus1)

		message_send = can.Message(arbitration_id = 0x100, is_extended_id = False, data = b"\x11\x22\x33\x44")
		network.send(message_send)

		message_recv = bus2.recv()
		self.assertEqual(message_recv.arbitration_id, message_send.arbitration_id)
		self.assertEqual(message_recv.is_extended_id, message_send.is_extended_id)
		self.assertEqual(message_recv.data, message_send.data)

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

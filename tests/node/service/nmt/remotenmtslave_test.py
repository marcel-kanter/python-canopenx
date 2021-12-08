import can
import struct
import time
import unittest

from canopenx import ObjectDictionary, Node, Network
from canopenx.nmt.states import *
from canopenx.node.service.nmt import RemoteNMTSlave


class RemoteNMTSlaveTestCase(unittest.TestCase):
	def test_properties(self):
		examinee = RemoteNMTSlave()

		self.assertEqual(examinee.state, INITIALIZING)

		with self.assertRaises(AttributeError):
			examinee.state = INITIALIZING

	def test_error_control(self):
		bus1 = can.Bus(interface = "virtual", channel = 0)
		bus2 = can.Bus(interface = "virtual", channel = 0)
		network = Network()
		dictionary = ObjectDictionary()
		node = Node(10, dictionary)
		examinee = RemoteNMTSlave()

		network.connect(bus1)
		network.add(node)
		examinee.attach(node)

		self.assertEqual(examinee.state, 0x00)

		#### Test step: Remote message -> Drop message
		message = can.Message(arbitration_id = 0x70A, is_extended_id = False, is_remote_frame = True, dlc = 1)
		bus2.send(message)
		time.sleep(0.01)

		self.assertEqual(examinee.state, 0x00)

		#### Test step: Missing data -> Drop message
		message = can.Message(arbitration_id = 0x70A, is_extended_id = False, data = b"")
		bus2.send(message)
		time.sleep(0.01)

		self.assertEqual(examinee.state, 0x00)

		#### Test step: Too much data -> Drop message
		message = can.Message(arbitration_id = 0x70A, is_extended_id = False, data = b"\x05\x05")
		bus2.send(message)
		time.sleep(0.01)

		self.assertEqual(examinee.state, 0x00)

		#### Test step: Remote message -> Drop message
		message = can.Message(arbitration_id = 0x70A, is_extended_id = False, is_remote_frame = True, dlc = 1)
		bus2.send(message)
		time.sleep(0.01)

		self.assertEqual(examinee.state, 0x00)

		#### Test step: NMT state with toggle bit
		message = can.Message(arbitration_id = 0x70A, is_extended_id = False, data = b"\x85")
		bus2.send(message)
		time.sleep(0.01)

		self.assertEqual(examinee.state, 0x05)

		#### Test step: NMT state without toggle bit
		message = can.Message(arbitration_id = 0x70A, is_extended_id = False, data = b"\x04")
		bus2.send(message)
		time.sleep(0.01)

		self.assertEqual(examinee.state, 0x04)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_node_control(self):
		bus1 = can.Bus(interface = "virtual", channel = 0)
		bus2 = can.Bus(interface = "virtual", channel = 0)
		dictionary = ObjectDictionary()
		node_id = 10
		node = Node(10, dictionary)
		examinee = RemoteNMTSlave()
		network = Network()

		network.add(node)
		examinee.attach(node)
		network.connect(bus1)

		#### Test step: Unknown state value -> ValueError
		with self.assertRaises(ValueError):
			examinee.state = 0xFF

		#### Test step: Reset application
		examinee.state = INITIALIZING

		message_recv = bus2.recv(0.1)
		self.assertEqual(message_recv.arbitration_id, 0x00)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<BB", 0x81, node_id))

		#### Test step: Enter preoperational
		examinee.state = PRE_OPERATIONAL

		message_recv = bus2.recv(0.1)
		self.assertEqual(message_recv.arbitration_id, 0x00)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<BB", 0x80, node_id))

		#### Test step: Operational
		examinee.state = OPERATIONAL

		message_recv = bus2.recv(0.1)
		self.assertEqual(message_recv.arbitration_id, 0x00)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<BB", 0x01, node_id))

		#### Test step: Stopped
		examinee.state = STOPPED

		message_recv = bus2.recv(0.1)
		self.assertEqual(message_recv.arbitration_id, 0x00)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<BB", 0x02, node_id))

		#### Test step: Reset communication
		examinee.reset_communication()

		message_recv = bus2.recv(0.1)
		self.assertEqual(message_recv.arbitration_id, 0x00)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<BB", 0x82, node_id))

		#### Test step: Manual send command
		with self.assertRaises(ValueError):
			examinee.send_command(-1)

		with self.assertRaises(ValueError):
			examinee.send_command(256)

		examinee.send_command(0x81)
		message_recv = bus2.recv(0.1)
		self.assertEqual(message_recv.arbitration_id, 0x00)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<BB", 0x81, node_id))

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

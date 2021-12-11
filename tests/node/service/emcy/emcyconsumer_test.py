import can
import mock
import struct
import time
import unittest

from canopenx import ObjectDictionary, Network, Node
from canopenx.node.service.emcy import EMCYConsumer, EMCYEvent


class EMCYConsumerTestCase(unittest.TestCase):
	def test_on_emcy(self):
		bus1 = can.Bus(interface = "virtual", channel = 0)
		bus2 = can.Bus(interface = "virtual", channel = 0)
		network = Network()
		dictionary = ObjectDictionary()
		node = Node(10, dictionary)
		examinee = EMCYConsumer()

		network.connect(bus1)
		network.add(node)
		
		examinee.attach(node)

		cb1 = mock.Mock()
		examinee.add_callback("emcy", cb1)

		#### Test step: EMCY write no error, or error reset
		with self.subTest("EMCY write no error, or error reset"):
			cb1.reset_mock()
			d = struct.pack("<HB5s", 0x0000, 0x00, b"\x00\x00\x00\x00\x00")
			message = can.Message(arbitration_id = 0x80 + node.id, is_extended_id = False, data = d)
			bus2.send(message)
			time.sleep(0.001)
			cb1.assert_called_once_with(EMCYEvent(0x0000, 0x00, b"\x00\x00\x00\x00\x00"))

		#### Test step: EMCY write with differing extended frame bit
		with self.subTest("EMCY write with differing extended frame bit"):
			cb1.reset_mock()
			d = struct.pack("<HB5s", 0x0001, 0x00, b"\x00\x00\x00\x00\x00")
			message = can.Message(arbitration_id = 0x80 + node.id, is_extended_id = True, data = d)
			bus2.send(message)
			time.sleep(0.1)
			cb1.assert_not_called()

		#### Test step: EMCY write with malformed message - too short message
		with self.subTest("EMCY write with malformed message - too short message"):
			cb1.reset_mock()
			d = struct.pack("<HB4s", 0x0002, 0x00, b"\x00\x00\x00\x00")
			message = can.Message(arbitration_id = 0x80 + node.id, is_extended_id = False, data = d)
			bus2.send(message)
			time.sleep(0.1)
			cb1.assert_not_called()

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

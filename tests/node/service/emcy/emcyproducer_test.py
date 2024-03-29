import can
import struct
import unittest

from canopenx import ObjectDictionary, Network, Node
from canopenx.emcy.errorcodes import NO_ERROR, GENERIC_ERROR, SOFTWARE_ERROR
from canopenx.node.service.emcy import EMCYProducer


class EMCYProducerTestCase(unittest.TestCase):
	def test_send(self):
		bus1 = can.Bus(interface = "virtual", channel = 0)
		bus2 = can.Bus(interface = "virtual", channel = 0)
		network = Network()
		dictionary = ObjectDictionary()
		node = Node(10, dictionary)
		examinee = EMCYProducer()

		network.connect(bus1)
		network.add(node)

		examinee.attach(node)

		#### Test step: Invalid value ranges
		error_register = 0
		data = None
		for error_code in [-1, -100, 0x10000]:
			with self.assertRaises(ValueError):
				examinee.send(error_code, error_register, data)

		error_code = 0
		data = None
		for error_register in [-1, -100, 0x100]:
			with self.assertRaises(ValueError):
				examinee.send(error_code, error_register, data)

		error_code = 0
		error_register = 0
		data = b"\x01\x02\x03\x04\x05\x06"
		with self.assertRaises(ValueError):
			examinee.send(error_code, error_register, data)

		#### Test step: Send error without data
		error_code = 0
		error_register = 0
		data = None
		examinee.send(error_code, error_register, data)
		message_recv = bus2.recv(1)
		self.assertEqual(message_recv.arbitration_id, 0x80 + node.id)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<HB5s", error_code, error_register, b"\x00\x00\x00\x00\x00"))

		#### Test step: Send error with some data
		error_code = 0
		error_register = 0
		data = b"\x01\x02"
		examinee.send(error_code, error_register, data)
		message_recv = bus2.recv(1)
		self.assertEqual(message_recv.arbitration_id, 0x80 + node.id)
		self.assertEqual(message_recv.is_extended_id, False)
		self.assertEqual(message_recv.data, struct.pack("<HB5s", error_code, error_register, b"\x01\x02\x00\x00\x00"))

		#### Test step: Send some error_codes
		test_data = [(NO_ERROR, 0x00), (GENERIC_ERROR, 0x10), (SOFTWARE_ERROR, 0x14)]
		for value in test_data:
			with self.subTest(value = value):
				error_code = value[0]
				error_register = value[1]
				data = b"\x01\x02"
				examinee.send(error_code, error_register, data)
				message_recv = bus2.recv(1)
				self.assertEqual(message_recv.arbitration_id, 0x80 + node.id)
				self.assertEqual(message_recv.is_extended_id, False)
				self.assertEqual(message_recv.data, struct.pack("<HB5s", error_code, error_register, b"\x01\x02\x00\x00\x00"))

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

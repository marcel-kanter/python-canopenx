import can
import struct
import sys
import threading
import unittest

from canopenx import Network, Node
from canopenx.objectdictionary import ObjectDictionary, Variable
from canopenx.objectdictionary.datatypes import UNSIGNED16, UNSIGNED64
from canopenx.node.service.sdo import SDOClient


class SDOClientTestCase(unittest.TestCase):
	def run(self, result = None):
		# Save a reference to the result, the helper threads use them
		if result == None:
			self.result = self.defaultTestResult()
		else:
			self.result = result

		unittest.TestCase.run(self, self.result)

		return self.result

	def test_expedited_download(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		helper = threading.Thread(target = handle_expedited_download, args = (self, bus2), daemon = True)

		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		helper.start()

		node.sdo.download(0x1000, 0x00, b"\x01\x00")

		helper.join(1.0)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_expedited_upload(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		helper = threading.Thread(target = handle_expedited_upload, args = (self, bus2), daemon = True)

		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		helper.start()

		node.sdo.upload(0x1000, 0x00)

		helper.join(1.0)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_segmented_download(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		helper = threading.Thread(target = handle_segmented_download, args = (self, bus2), daemon = True)

		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		helper.start()

		node.sdo.download(0x2000, 0x00, b"\x01\x00\x00\x00\x00\x00\x00\x00")

		helper.join(1.0)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_segmented_upload(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		helper = threading.Thread(target = handle_segmented_upload, args = (self, bus2), daemon = True)

		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		helper.start()

		node.sdo.upload(0x2000, 0x00)

		helper.join(1.0)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()


class ServiceTestNode(Node):
	def __init__(self):
		dictionary = ObjectDictionary()
		dictionary.add(Variable("short", 0x1000, 0x00, UNSIGNED16))
		dictionary.add(Variable("long", 0x2000, 0x00, UNSIGNED64))
		Node.__init__(self, 10, dictionary)
		self.sdo = SDOClient()

	def attach(self, network):
		Node.attach(self, network)
		self.sdo.attach(self)

	def detach(self):
		self.sdo.detach()
		Node.detach(self)


def handle_expedited_download(testcase, bus):
	try:
		# Initiate Download Request
		message = bus.recv(timeout = 1.0)
		testcase.assertEqual(message.arbitration_id, 0x60A)
		testcase.assertEqual(message.data, b"\x2B\x00\x10\x00\x01\x00\x00\x00")

		# Initiate Download Confirmation
		index = 0x1000
		subindex = 0x00
		d = struct.pack("<BHB4s", 0x60, index, subindex, b"\x00\x00\x00\x00")
		message = can.Message(arbitration_id = 0x58A, is_extended_id = False, data = d)
		bus.send(message)
	except AssertionError:
		testcase.result.addFailure(testcase, sys.exc_info())
	except:
		testcase.result.addError(testcase, sys.exc_info())


def handle_expedited_upload(testcase, bus):
	try:
		# Initiate Upload Request
		message = bus.recv(timeout = 1.0)
		testcase.assertEqual(message.arbitration_id, 0x60A)
		testcase.assertEqual(message.data, b"\x40\x00\x10\x00\x00\x00\x00\x00")

		# Initiate Upload Confirmation
		index = 0x1000
		subindex = 0x00
		data = b"\x01\x00\x00\x00"
		d = struct.pack("<BHB4s", 0x4B, index, subindex, data)
		message = can.Message(arbitration_id = 0x58A, is_extended_id = False, data = d)
		bus.send(message)
	except AssertionError:
		testcase.result.addFailure(testcase, sys.exc_info())
	except:
		testcase.result.addError(testcase, sys.exc_info())


def handle_segmented_download(testcase, bus):
	try:
		# Initiate Download Request
		message = bus.recv(timeout = 1.0)
		testcase.assertEqual(message.arbitration_id, 0x60A)
		testcase.assertEqual(message.data, b"\x21\x00\x20\x00\x08\x00\x00\x00")

		# Initiate Download Confirmation
		index = 0x1000
		subindex = 0x00
		d = struct.pack("<BHB4s", 0x60, index, subindex, b"\x00\x00\x00\x00")
		message = can.Message(arbitration_id = 0x58A, is_extended_id = False, data = d)
		bus.send(message)
	except AssertionError:
		testcase.result.addFailure(testcase, sys.exc_info())
	except:
		testcase.result.addError(testcase, sys.exc_info())


def handle_segmented_upload(testcase, bus):
	try:
		# Initiate Upload Request
		message = bus.recv(timeout = 1.0)
		testcase.assertEqual(message.arbitration_id, 0x60A)
		testcase.assertEqual(message.data, b"\x40\x00\x20\x00\x00\x00\x00\x00")

		# Initiate Upload Confirmation
		index = 0x1000
		subindex = 0x00
		data = 8
		d = struct.pack("<BHBL", 0x41, index, subindex, data)
		message = can.Message(arbitration_id = 0x58A, is_extended_id = False, data = d)
		bus.send(message)
	except AssertionError:
		testcase.result.addFailure(testcase, sys.exc_info())
	except:
		testcase.result.addError(testcase, sys.exc_info())

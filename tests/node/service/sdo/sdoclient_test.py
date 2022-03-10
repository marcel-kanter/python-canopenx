import can
import unittest

from canopenx import Network, Node
from canopenx.objectdictionary import ObjectDictionary, Variable
from canopenx.objectdictionary.datatypes import UNSIGNED16, UNSIGNED64
from canopenx.node.service.sdo import SDOClient


class SDOClientTestCase(unittest.TestCase):
	def test_expedited_download(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_expedited_upload(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_segmented_download(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

		network.disconnect()
		bus1.shutdown()
		bus2.shutdown()

	def test_segmented_upload(self):
		bus1 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		bus2 = can.ThreadSafeBus(interface = "virtual", channel = 0)
		network = Network()
		network.connect(bus1)

		node = ServiceTestNode()
		network.add(node)

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

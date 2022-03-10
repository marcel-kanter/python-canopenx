from .node import Node
from .service.nmt import LocalNMTSlave
from .service.emcy import EMCYProducer
from .service.sdo import SDOServer


class LocalNode(Node):
	""" Representation of a local CANopen node.

	This class represents a local CANopen node and can be accessed by other nodes on the bus.
	"""
	def __init__(self, node_id, dictionary):
		Node.__init__(self, node_id, dictionary)
		self.nmt = LocalNMTSlave()
		self.emcy = EMCYProducer()
		self.sdo = SDOServer()

	def attach(self, network):
		Node.attach(self, network)
		self.nmt.attach(self)
		self.emcy.attach(self)
		self.sdo.attach(self)

	def detach(self):
		self.sdo.detach()
		self.emcy.detach()
		self.nmt.detach()
		Node.detach(self)

from .node import Node
from .service.nmt import LocalNMTSlave


class LocalNode(Node):
	""" Representation of a local CANopen node.

	This class represents a local CANopen node and can be accessed by other nodes on the bus.
	"""
	def __init__(self, node_id, dictionary):
		Node.__init__(self, node_id, dictionary)
		self.nmt = LocalNMTSlave()

	def attach(self, network):
		Node.attach(self, network)
		self.nmt.attach(self)

	def detach(self):
		self.nmt.detach()
		Node.detach(self)

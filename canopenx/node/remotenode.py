from .node import Node
from .service.nmt import RemoteNMTSlave
from .service.emcy import EMCYConsumer


class RemoteNode(Node):
	""" Representation of a remote CANopen node.

	This class represents a remote CANopen node and can be used to access the node on the bus.
	"""
	def __init__(self, node_id, dictionary):
		Node.__init__(self, node_id, dictionary)
		self.nmt = RemoteNMTSlave()
		self.emcy = EMCYConsumer()

	def attach(self, network):
		Node.attach(self, network)
		self.nmt.attach(self)
		self.emcy.attach(self)

	def detach(self):
		self.emcy.detach()
		self.nmt.detach()
		Node.detach(self)

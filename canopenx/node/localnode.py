from .node import Node


class LocalNode(Node):
	""" Representation of a local CANopen node.

	This class represents a local CANopen node and can be accessed by other nodes on the bus.
	"""
	def __init__(self, node_id, dictionary):
		Node.__init__(self, node_id, dictionary)

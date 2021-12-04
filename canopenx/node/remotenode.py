from .node import Node


class RemoteNode(Node):
	""" Representation of a remote CANopen node.

	This class represents a remote CANopen node and can be used to access the node on the bus.
	"""
	def __init__(self, node_id, dictionary):
		Node.__init__(self, node_id, dictionary)

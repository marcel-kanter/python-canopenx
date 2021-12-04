class Service(object):
	""" Service

	This class is the base class for all services of a node.
	"""

	__slots__ = ["_node"]

	def __init__(self):
		self._node = None

	def attach(self, node):
		""" Attach handler.

		Must be called when the node gets attached to the network.
		"""
		if self.is_attached():
			self.detach()
		self._node = node

	def detach(self):
		""" Detach handler.

		Must be called when the node gets detached from the network.
		"""
		self._node = None

	def is_attached(self):
		""" Returns True if the service is attached.
		"""
		return self._node is not None

	@property
	def node(self):
		""" Returns the node this service belongs to or None if the service is not attached.
		"""
		return self._node

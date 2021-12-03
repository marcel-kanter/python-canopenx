class Node(object):
	__slots__ = ["_dictionary", "_id", "_name", "_network"]

	def __eq__(self, other):
		""" Indicates whether some other object is "equal to" this one.
		"""
		if type(self) != type(other):
			return False
		return self is other or (self._dictionary == other._dictionary and self._id == other._id and self._name == other._name)

	def __init__(self, node_id, dictionary, name = None):
		"""
		:param node_id: The node id of this Node. Must be in range 1 .. 127.

		:param dictionary: The object dictionary describing the node.

		:param name: The name of the Node. Will be converted to a string.

		:raises: ValueError
		"""
		if int(node_id) < 1 or int(node_id) > 127:
			raise ValueError("The node_id is out of range 1 ... 127.")

		self._id = int(node_id)
		if name is None:
			self._name = None
		else:
			self._name = str(name)
		self._dictionary = dictionary
		self._network = None

	def attach(self, network):
		""" Attach a Node to a Network. Detaches if the Node is already attached to a Network.

		:param network: The Network to which the Node should be attached to.
		"""
		if self.is_attached():
			self.detach()
		self._network = network

	@property
	def dictionary(self):
		return self._dictionary

	def detach(self):
		""" Detach the Node from a Network.
		"""
		self._network = None

	@property
	def id(self):
		return self._id

	def is_attached(self):
		""" Returns True if the Node is attached to a Network.
		"""
		return self._network is not None

	@property
	def name(self):
		return self._name

	@property
	def network(self):
		return self._network

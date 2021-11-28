class Node(object):
	__slots__ = ["_id", "_name"]

	def __eq__(self, other):
		""" Indicates whether some other object is "equal to" this one.
		"""
		if type(self) != type(other):
			return False
		return self is other or (self._id == other._id and self._name == other._name)

	def __init__(self, node_id, name = None):
		"""
		:param node_id: The node id of this Node. Must be in range 1 .. 127.

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

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name
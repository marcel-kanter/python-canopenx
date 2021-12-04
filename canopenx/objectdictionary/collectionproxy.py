class CollectionProxy(object):

	__slots__ = ["_node", "_original"]

	def __contains__(self, key):
		""" Returns True if the proxied object contains an item with the specified subindex or name.
		"""
		return key in self._original

	def __getitem__(self, key):
		""" Returns the item identified by the name or the subindex.
		"""
		return self._original[key].proxy(self._node)

	def __iter__(self):
		""" Returns an iterator over all items in the proxied object.
		"""
		return iter(self._original)

	def __init__(self, original, node):
		self._original = original
		self._node = node

	def __len__(self):
		""" Returns the number of items in the proxied object.
		"""
		return len(self._original)

	@property
	def data_type(self):
		""" Returns the data type of the proxied object.
		"""
		return self._original._data_type

	@property
	def index(self):
		""" Returns the index of the proxied object.
		"""
		return self._original._index

	@property
	def name(self):
		""" Returns the name of the proxied object.
		"""
		return self._original._name

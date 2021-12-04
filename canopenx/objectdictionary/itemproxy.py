class ItemProxy(object):

	__slots__ = ["_node", "_original"]

	def __init__(self, original, node):
		self._original = original
		self._node = node

	@property
	def access_type(self):
		""" Returns the access type as defined in DS301 v4.02 Table 43: Access attributes for data objects.
		"""
		return self._original._access_type

	@property
	def data_type(self):
		""" Returns the data type as defined in DS301 v4.02 Table 44: Object dictionary data types.
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

	@property
	def subindex(self):
		""" Returns the sub-index of the proxied object.
		"""
		return self._original._subindex

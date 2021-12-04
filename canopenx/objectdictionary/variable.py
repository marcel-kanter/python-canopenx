from .datatypes import *
from .itemproxy import ItemProxy


class Variable(object):
	__slots__ = ["_name", "_index", "_subindex", "_data_type", "_access_type"]

	__sizes = {BOOLEAN: 1, INTEGER8: 8, INTEGER16: 16, INTEGER32: 32, UNSIGNED8: 8, UNSIGNED16: 16, UNSIGNED32: 32, REAL32: 32, VISIBLE_STRING: 0, OCTET_STRING: 0, UNICODE_STRING: 0, TIME_OF_DAY: 48, TIME_DIFFERENCE: 48, DOMAIN: 0, INTEGER24: 24, REAL64: 64, INTEGER40: 40, INTEGER48: 48, INTEGER56: 56, INTEGER64: 64, UNSIGNED24: 24, UNSIGNED40: 40, UNSIGNED48: 48, UNSIGNED56: 56, UNSIGNED64: 64}

	def __eq__(self, other):
		""" Indicates whether some other object is "equal to" this Variable.
		"""
		if type(self) != type(other):
			return False
		return self is other or (self._name == other._name and self._index == other._index and self._subindex == other._subindex and self._data_type == other._data_type and self._access_type == other._access_type)

	def __init__(self, name, index, subindex, data_type, access_type = "rw"):
		"""
		:param name: A string. The name of this variable.

		:param index: An integer. Must be in range 0x0000 .. 0xFFFF

		:param subindex: An integer. Must be in range 0x00 .. 0xFF

		:param data_type: An integer. Must be one of the allowed data types.

		:param access_type: A string. Must be one of "rw", "wo", "ro", "const".

		:raises: ValueError
		"""
		if index < 0x0000 or index > 0xFFFF:
			raise ValueError("The specified index is not in range 0x0000 .. 0xFFFF.")
		if subindex < 0x00 or subindex > 0xFF:
			raise ValueError("The specified subindex is not in range 0x00 .. 0xFF.")
		if data_type not in self.__sizes:
			raise ValueError("The specified data_type is not allowed.")
		if access_type not in ["rw", "wo", "ro", "const"]:
			raise ValueError("The specified access_type is not one of \"rw\", \"wo\", \"ro\", \"const\".")

		self._name = str(name)
		self._index = int(index)
		self._subindex = int(subindex)
		self._data_type = int(data_type)
		self._access_type = str(access_type)

	@property
	def access_type(self):
		""" Returns the access type as defined in DS301 v4.02 Table 43: Access attributes for data objects.
		"""
		return self._access_type

	@access_type.setter
	def access_type(self, x):
		if x not in ["rw", "wo", "ro", "const"]:
			raise ValueError("The specified access_type is not one of \"rw\", \"wo\", \"ro\", \"const\".")
		self._access_type = x

	@property
	def data_type(self):
		""" Returns the data type as defined in DS301 v4.02 Table 44: Object dictionary data types.
		"""
		return self._data_type

	@property
	def index(self):
		""" Returns the index of the Variable.
		"""
		return self._index

	@property
	def name(self):
		""" Returns the name of the Variable.
		"""
		return self._name

	def proxy(self, node):
		""" Returns a proxy bound to a specific node.
		"""
		return ItemProxy(self, node)

	@property
	def size(self):
		""" Returns the size of the Variable in bits as described in DS301 v4.2 chapter 7.4.7 Data type entry usage.
		For variables with variable length (VISIBLE_STRING, OCTET_STRING, UNICODE_STRING and DOMAIN) it returns 0.
		"""
		return self.__sizes[self.data_type]

	@property
	def subindex(self):
		""" Returns the sub-index of the Variable.
		"""
		return self._subindex

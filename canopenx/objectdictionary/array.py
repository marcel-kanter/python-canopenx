from .domain import Domain
from .variable import Variable
from .collectionproxy import CollectionProxy
from canopenx.objectdictionary import objecttypes


class Array(object):
	""" Representation of an object of type ARRAY

	This class is the representation of an ARRAY of a object dictionary. It is a mutable auto-associative mapping and may contain zero or more variables.
	"""

	object_type = objecttypes.ARRAY

	__slots__ = ["_name", "_index", "_data_type", "_items_subindex", "_items_name"]

	def __contains__(self, key):
		""" Returns True if the Array contains an item with the specified subindex or name.
		"""
		try:
			self[key]
		except:
			return False
		else:
			return True

	def __delitem__(self, key):
		""" Removes the item identified by the name or the subindex from the Array.
		"""
		item = self[key]
		del self._items_subindex[item.subindex]
		del self._items_name[item.name]

	def __eq__(self, other):
		""" Indicates whether some other object is "equal to" this one.
		"""
		if type(self) != type(other):
			return False
		return self is other or (self._name == other._name and self._index == other._index and self._data_type == other._data_type and self._items_subindex == other._items_subindex)

	def __getitem__(self, key):
		""" Returns the item identified by the name or the subindex.
		"""
		try:
			return self._items_subindex[key]
		except KeyError:
			try:
				return self._items_name[key]
			except:
				raise KeyError("The specified item was not found.")

	def __iter__(self):
		""" Returns an iterator over all items in the Array.
		"""
		return iter(self._items_subindex.values())

	def __init__(self, name, index, data_type):
		"""
		:param name: A string. The name of this Array.

		:param index: An integer. Must be in range 0x0000 .. 0xFFFF

		:param data_type: An integer. Must be one of the allowed standard datatypes in range 0x00 .. 0x1F

		:raises: ValueError
		"""
		if index < 0x0000 or index > 0xFFFF:
			raise ValueError("The specified index is not in range 0x0000 .. 0xFFFF.")
		if data_type < 0x0000 or data_type > 0x1F:
			raise ValueError("The specified data_type is not in range 0x00 .. 0x1F.")

		self._name = str(name)
		self._index = int(index)
		self._data_type = int(data_type)

		self._items_subindex = {}
		self._items_name = {}

	def __len__(self):
		""" Returns the number of items in the Array.
		"""
		return len(self._items_subindex)

	def add(self, item):
		""" Adds an item to the Array. It may be accessed later by the name or the subindex.

		:param item: The item to add. Must be a Variable.
		"""
		if not isinstance(item, Variable) or isinstance(item, Domain):
			raise TypeError("This type of item is not supported.")
		if item.subindex in self._items_subindex or item.name in self._items_name:
			raise ValueError("A item with this subindex or name is already in the Array.")
		if item.index != self.index:
			raise ValueError("The index of the item must match the index of the Array.")

		self._items_subindex[item.subindex] = item
		self._items_name[item.name] = item

	@property
	def data_type(self):
		""" Returns the data type of the Array.
		"""
		return self._data_type

	@property
	def index(self):
		""" Returns the index of the Array.
		"""
		return self._index

	@property
	def name(self):
		""" Returns the name of the Array.
		"""
		return self._name

	def proxy(self, node):
		""" Returns a proxy bound to a specific node.
		"""
		return CollectionProxy(self, node)

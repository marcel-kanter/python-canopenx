from .variable import Variable


class ObjectDictionary(object):
	__slots__ = ["_items_index", "_items_name"]

	def __contains__(self, key):
		""" Returns True if the object dictionary contains an item with the specified index or name.
		"""
		try:
			self[key]
		except:
			return False
		else:
			return True

	def __delitem__(self, key):
		""" Removes the item identified by the name or the index from the object dictionary.
		"""
		item = self[key]
		del self._items_index[item.index]
		del self._items_name[item.name]

	def __eq__(self, other):
		""" Indicates whether some other object is "equal to" this one.
		"""
		if type(self) != type(other):
			return False
		return self is other or (self._items_index == other._items_index)

	def __getitem__(self, key):
		""" Returns the item identified by the name or the index.
		"""
		if key in self._items_index:
			return self._items_index[key]
		if key in self._items_name:
			return self._items_name[key]
		raise KeyError("The specified item was not found.")

	def __iter__(self):
		""" Returns an iterator over all items in the object dictionary.
		"""
		return iter(self._items_index.values())

	def __init__(self):
		self._items_index = {}
		self._items_name = {}

	def __len__(self):
		""" Returns the number of items in the object dictionary.
		"""
		return len(self._items_index)

	def add(self, item):
		""" Adds an item to the object dictionary. It may be accessed later by the name or the index.

		:param item: The item to add. Must be an Variable.
		"""
		if not isinstance(item, Variable):
			raise TypeError("This type of item is not supported.")
		if item.index in self._items_index or item.name in self._items_name:
			raise ValueError("A item with this index or name is already in the object dictionary.")

		self._items_index[item.index] = item
		self._items_name[item.name] = item

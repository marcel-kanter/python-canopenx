from .array import Array
from .datatypes import UNSIGNED8, UNSIGNED16, UNSIGNED32
from .variable import Variable
from canopenx.objectdictionary import objecttypes


class DefStruct(Array):
	"""  Representation of an object of type DEFSTRUCT

	This class is the representation of a DEFSTRUCT of an object dictionary. It is a mutable auto-associative mapping and may contain zero or more variables.
	"""

	object_type = objecttypes.DEFSTRUCT

	def __init__(self, name, index):
		"""
		:param name: A string. The name of this variable.

		:param index: An integer. Must be in range 0x0000 .. 0xFFFF

		:raises: TypeError, ValueError
		"""
		Array.__init__(self, name, index, UNSIGNED16)

	def add(self, item):
		if not isinstance(item, Variable):
			raise TypeError("This type of item is not supported.")

		if item.subindex == 0x00:
			if item.data_type != UNSIGNED8:
				raise ValueError("The data type of the item at subindex 0x00 must be UNSIGNED8.")
		elif item.subindex == 0xFF:
			if item.data_type != UNSIGNED32:
				raise ValueError("The data type of the item at subindex 0xFF must be UNSIGNED32.")
		else:
			if item.data_type != UNSIGNED16:
				raise ValueError("The data type of the item at subindex 0x01 .. 0xFE must be UNSIGNED16.")

		Array.add(self, item)

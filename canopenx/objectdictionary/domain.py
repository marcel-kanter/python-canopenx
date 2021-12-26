from .variable import Variable
from canopenx.objectdictionary import datatypes, objecttypes


class Domain(Variable):
	"""  Representation of an object of type DOMAIN

	This class is a representation of a Domain object of an object dictionary. Basically this is a Variable with fixed subindex and data_type.
	"""

	object_type = objecttypes.DOMAIN

	def __init__(self, name, index, access_type = "rw"):
		"""
		:param name: A string. The name of this variable.

		:param index: An integer. Must be in range 0x0000 .. 0xFFFF

		:param subindex: An integer. Must be in range 0x00 .. 0xFF

		:param access_type: A string. Must be one of "rw", "wo", "ro", "const".

		:raises: ValueError
		"""
		Variable.__init__(self, name, index, 0x00, datatypes.DOMAIN, access_type)

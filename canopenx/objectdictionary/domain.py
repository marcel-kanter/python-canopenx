from .datatypes import DOMAIN
from .variable import Variable


class Domain(Variable):
	def __init__(self, name, index, access_type = "rw"):
		"""
		:param name: A string. The name of this variable.

		:param index: An integer. Must be in range 0x0000 .. 0xFFFF

		:param subindex: An integer. Must be in range 0x00 .. 0xFF

		:param access_type: A string. Must be one of "rw", "wo", "ro", "const".

		:raises: ValueError
		"""
		Variable.__init__(self, name, index, 0x00, DOMAIN, access_type)

import calendar
import struct
from .datatypes import *
from .itemproxy import ItemProxy


class Variable(object):
	__slots__ = ["_name", "_index", "_subindex", "_data_type", "_access_type", "_default_value"]

	__canopen_epoch = calendar.timegm((1984, 1, 1, 0, 0, 0))
	__sizes = {BOOLEAN: 1, INTEGER8: 8, INTEGER16: 16, INTEGER32: 32, UNSIGNED8: 8, UNSIGNED16: 16, UNSIGNED32: 32, REAL32: 32, VISIBLE_STRING: 0, OCTET_STRING: 0, UNICODE_STRING: 0, TIME_OF_DAY: 48, TIME_DIFFERENCE: 48, DOMAIN: 0, INTEGER24: 24, REAL64: 64, INTEGER40: 40, INTEGER48: 48, INTEGER56: 56, INTEGER64: 64, UNSIGNED24: 24, UNSIGNED40: 40, UNSIGNED48: 48, UNSIGNED56: 56, UNSIGNED64: 64}

	def __eq__(self, other):
		""" Indicates whether some other object is "equal to" this Variable.
		"""
		if type(self) != type(other):
			return False
		return self is other or (self._name == other._name and self._index == other._index and self._subindex == other._subindex and self._data_type == other._data_type and self._access_type == other._access_type)

	def __init__(self, name, index, subindex, data_type, access_type = "rw", default_value = None):
		"""
		:param name: A string. The name of this variable.

		:param index: An integer. Must be in range 0x0000 .. 0xFFFF

		:param subindex: An integer. Must be in range 0x00 .. 0xFF

		:param data_type: An integer. Must be one of the allowed data types.

		:param access_type: A string. Must be one of "rw", "wo", "ro", "const".

		:param default_value: The default value for this variable.

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

		if default_value is None:
			if data_type == BOOLEAN:
				default_value = False
			elif data_type in [REAL32, REAL64]:
				default_value = 0.0	
			elif data_type in [VISIBLE_STRING, OCTET_STRING, UNICODE_STRING]:
				default_value = ""
			elif data_type == DOMAIN:
				default_value = b""
			elif data_type == TIME_OF_DAY:
				default_value = self.__canopen_epoch
			else:
				default_value = 0

		self._name = str(name)
		self._index = int(index)
		self._subindex = int(subindex)
		self._data_type = int(data_type)
		self._access_type = str(access_type)

		try:
			self.encode(default_value)
		except ValueError:
			raise ValueError("The specfied default_value cannot be encoded with the specified data type.")
		self._default_value = default_value

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

	def decode(self, data):
		""" Returns the value for the given byte-like CANopen representation, depending on the type of the CANopen variable.

		:raises: ValueError
		"""
		value = None

		try:
			if self._data_type == BOOLEAN:
				value, = struct.unpack_from("<?", data)

			if self._data_type == INTEGER8:
				value, = struct.unpack_from("<b", data)

			if self._data_type == INTEGER16:
				value, = struct.unpack_from("<h", data)

			if self._data_type == INTEGER32:
				value, = struct.unpack_from("<l", data)

			if self._data_type == UNSIGNED8:
				value, = struct.unpack_from("<B", data)

			if self._data_type == UNSIGNED16:
				value, = struct.unpack_from("<H", data)

			if self._data_type == UNSIGNED32:
				value, = struct.unpack_from("<L", data)

			if self._data_type == REAL32:
				value, = struct.unpack_from("<f", data)

			if self._data_type == VISIBLE_STRING:
				value = bytes.decode(data, "ascii", errors = "replace")

			if self._data_type == OCTET_STRING:
				value = bytes.decode(data, "utf-8", errors = "replace")

			if self._data_type == UNICODE_STRING:
				value = bytes.decode(data, "utf-16-le", errors = "replace")

			if self._data_type == TIME_OF_DAY:
				m, d = struct.unpack_from("<LH", data)
				m &= 0xFFFFFFF
				value = d * 24 * 60 * 60 + m / 1000 + self.__canopen_epoch

			if self._data_type == TIME_DIFFERENCE:
				m, d = struct.unpack_from("<LH", data)
				m &= 0xFFFFFFF
				value = d * 24 * 60 * 60 + m / 1000

			if self._data_type == DOMAIN:
				value = data

			if self._data_type == INTEGER24:
				if len(data) < 3:
					raise ValueError("Decoding requires a buffer of at least 3 bytes.")
				value = int.from_bytes(data[0:3], "little", signed = True)

			if self._data_type == REAL64:
				value, = struct.unpack_from("<q", data)

			if self._data_type == INTEGER40:
				if len(data) < 5:
					raise ValueError("Decoding requires a buffer of at least 5 bytes.")
				value = int.from_bytes(data[0:5], "little", signed = True)

			if self._data_type == INTEGER48:
				if len(data) < 6:
					raise ValueError("Decoding requires a buffer of at least 6 bytes.")
				value = int.from_bytes(data[0:6], "little", signed = True)

			if self._data_type == INTEGER56:
				if len(data) < 7:
					raise ValueError("Decoding requires a buffer of at least 7 bytes.")
				value = int.from_bytes(data[0:7], "little", signed = True)

			if self._data_type == INTEGER64:
				value, = struct.unpack_from("<q", data)

			if self._data_type == UNSIGNED24:
				if len(data) < 3:
					raise ValueError("Decoding requires a buffer of at least 3 bytes.")
				value = int.from_bytes(data[0:3], "little", signed = False)

			if self._data_type == UNSIGNED40:
				if len(data) < 5:
					raise ValueError("Decoding requires a buffer of at least 5 bytes.")
				value = int.from_bytes(data[0:5], "little", signed = False)

			if self._data_type == UNSIGNED48:
				if len(data) < 6:
					raise ValueError("Decoding requires a buffer of at least 6 bytes.")
				value = int.from_bytes(data[0:6], "little", signed = False)

			if self._data_type == UNSIGNED56:
				if len(data) < 7:
					raise ValueError("Decoding requires a buffer of at least 7 bytes.")
				value = int.from_bytes(data[0:7], "little", signed = False)

			if self._data_type == UNSIGNED64:
				value, = struct.unpack_from("<Q", data)
		except struct.error:
			raise ValueError("Could not decode the specified data. Maybe the data format does not match the data type of the Variable.")

		return value

	@property
	def default_value(self):
		""" Returns the default value for this Variable.
		"""
		return self._default_value

	@default_value.setter
	def default_value(self, x):
		try:
			self.encode(x)
		except ValueError:
			raise ValueError("The specfied default_value cannot be encoded with the specified data type.")
		self._default_value = x

	def encode(self, value):
		""" Returns the byte-like CANopen representation of the given value, depending on the type of the CANopen variable.

		:raises: ValueError
		"""
		data = b""

		try:
			if self._data_type == BOOLEAN:
				data = struct.pack("?", value)

			if self._data_type == INTEGER8:
				data = struct.pack("<b", value)

			if self._data_type == INTEGER16:
				data = struct.pack("<h", value)

			if self._data_type == INTEGER32:
				data = struct.pack("<l", value)

			if self._data_type == UNSIGNED8:
				data = struct.pack("<B", value)

			if self._data_type == UNSIGNED16:
				data = struct.pack("<H", value)

			if self._data_type == UNSIGNED32:
				data = struct.pack("<L", value)

			if self._data_type == REAL32:
				data = struct.pack("<f", value)

			if self._data_type == VISIBLE_STRING:
				data = str.encode(value, "ascii")

			if self._data_type == OCTET_STRING:
				data = str.encode(value, "utf-8")

			if self._data_type == UNICODE_STRING:
				data = str.encode(value, "utf-16-le")

			if self._data_type == TIME_OF_DAY:
				if value < self.__canopen_epoch:
					raise ValueError("Encoding times before CANopen epoch is not defined.")
				x = divmod(value - self.__canopen_epoch, 24 * 60 * 60)
				d = int(x[0])
				m = round(x[1] * 1000)
				data = struct.pack("<LH", m, d)

			if self._data_type == TIME_DIFFERENCE:
				if value < 0:
					value = -value
				x = divmod(value, 24 * 60 * 60)
				d = int(x[0])
				m = round(x[1] * 1000)
				data = struct.pack("<LH", m, d)

			if self._data_type == DOMAIN:
				data = bytes(value)

			if self._data_type == INTEGER24:
				data = int.to_bytes(value, 3, "little", signed = True)

			if self._data_type == REAL64:
				data = struct.pack("<d", value)

			if self._data_type == INTEGER40:
				data = int.to_bytes(value, 5, "little", signed = True)

			if self._data_type == INTEGER48:
				data = int.to_bytes(value, 6, "little", signed = True)

			if self._data_type == INTEGER56:
				data = int.to_bytes(value, 7, "little", signed = True)

			if self._data_type == INTEGER64:
				data = struct.pack("<q", value)

			if self._data_type == UNSIGNED24:
				data = int.to_bytes(value, 3, "little", signed = False)

			if self._data_type == UNSIGNED40:
				data = int.to_bytes(value, 5, "little", signed = False)

			if self._data_type == UNSIGNED48:
				data = int.to_bytes(value, 6, "little", signed = False)

			if self._data_type == UNSIGNED56:
				data = int.to_bytes(value, 7, "little", signed = False)

			if self._data_type == UNSIGNED64:
				data = struct.pack("<Q", value)
		except (struct.error, TypeError):
			raise ValueError("Could not encode the specified data. Maybe the data format does not match the data type of the Variable.")
		except OverflowError:
			raise ValueError("Could not encode the specified data. The value overflowed, maybe a negative value should be encoded as unsigned.")

		return data

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

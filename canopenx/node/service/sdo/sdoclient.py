import can
import struct
from ..service import Service


class SDOClient(Service):
	def attach(self, node):
		Service.attach(self, node)
		self._node.network.subscribe(0x580 + self._node.id, self.on_sdo_message)

	def detach(self):
		self._node.network.unsubscribe(0x580 + self._node.id, self.on_sdo_message)
		Service.detach(self)

	def download(self, index, subindex, data):
		"""
		:param index: integer
		:param subindex: integer
		:param data: bytes
		"""
		l = len(data)

		# Download of zero length data is not a normal use case, but is needed for erasing of strings.
		if l > 0 and l <= 4:
			# cmd = 1, e = 1, s = 1, n = 4 - l
			d = struct.pack("<BHB4s", 0x23 | (4 - l) << 2, index, subindex, data)
		else:
			# cmd = 1, e = 0, s = 1, n = 0
			d = struct.pack("<BHBL", 0x21, index, subindex, l)

		message = can.Message(arbitration_id = 0x600 + self._node.id, is_extended_id = False, data = d)
		self._node.network.send(message)

	def on_sdo_message(self, message):
		""" Handler for the responses from the SDO server.
		"""
		pass

	def upload(self, index, subindex):
		"""
		:param index: integer
		:param subindex: integer

		:returns: bytes
		"""
		# cmd = 2
		d = struct.pack("<BHB4s", 0x40, index, subindex, b"\x00\x00\x00\x00")
		message = can.Message(arbitration_id = 0x600 + self._node.id, is_extended_id = False, data = d)
		self._node.network.send(message)

		return b""

import can
import struct
from ..service import Service


class EMCYProducer(Service):
	""" EMCYProducer

	This class is an implementation of an EMCY producer.
	"""
	def __init__(self):
		Service.__init__(self)

	def send(self, error_code, error_register, data = None):
		""" Send an emcy message on the bus with the specified values.
		
		:param error_code: The error code to use.
		
		:param error_register: The value of the error register to send in the message.
		
		:param data: The data for the manufacturer specific data field.
		
		:raises: ValueError
		"""
		if error_code < 0x0000 or error_code > 0xFFFF:
			raise ValueError("The specified error_code is out of range 0x0000 .. 0xFFFF")
		if error_register < 0x00 or error_register > 0xFF:
			raise ValueError("The specified error register is out of range 0x00 .. 0xFF")
		if data == None:
			data = b"\x00\x00\x00\x00\x00"
		if len(data) > 5:
			raise ValueError("The emcy protocol allows only 5 bytes in the manufacturer specific error field.")

		d = struct.pack("<HB5s", error_code, error_register, data)
		message = can.Message(arbitration_id = 0x80 + self._node.id, is_extended_id = False, data = d)

		self._node.network.send(message)

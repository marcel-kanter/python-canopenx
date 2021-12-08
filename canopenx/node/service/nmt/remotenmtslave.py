import can
import struct
from .nmtservice import NMTService
from canopenx.nmt.states import *


class RemoteNMTSlave(NMTService):
	def __init__(self):
		NMTService.__init__(self)

	def attach(self, node):
		NMTService.attach(self, node)
		self._node.network.subscribe(0x700 + self._node.id, self.on_error_control)

	def detach(self):
		if not self.is_attached():
			raise RuntimeError("The RemoteNMTSlave is already detached.")

		self._node.network.unsubscribe(0x700 + self._node.id, self.on_error_control)
		NMTService.detach(self)

	def on_error_control(self, message):
		""" Handler for error control requests. It catches all status messages from the remote node and updates the state property. """
		if message.is_remote_frame:
			return
		if message.dlc != 1:
			return

		self._state = message.data[0] & 0x7F

	def reset_communication(self):
		""" Sends a NMT reset communication command to the node.
		"""
		self.send_command(0x82)

	def send_command(self, command):
		""" Sends a NMT command to the node.
		Raises ValueError if the command is out of range.

		:param command: The command to send.
			Must be an integer in the range 0x00 ... 0xFF

		:raises: ValueError
		"""
		if int(command) < 0x00 or int(command) > 0xFF:
			raise ValueError("The specified command is out of range 0x00 .. 0xFF.")

		d = struct.pack("<BB", command, self._node.id)
		request = can.Message(arbitration_id = 0x000, is_extended_id = False, data = d)
		self._node.network.send(request)

	@property
	def state(self):
		return self._state

	@state.setter
	def state(self, value):
		"""
		:param value: The new NMT state. Must be one of the valid states.

		:raises: ValueError
		"""
		if value == INITIALIZING:
			self.send_command(0x81)
		elif value == STOPPED:
			self.send_command(0x02)
		elif value == OPERATIONAL:
			self.send_command(0x01)
		elif value == PRE_OPERATIONAL:
			self.send_command(0x80)
		else:
			raise ValueError("The specified state is not a valid state.")

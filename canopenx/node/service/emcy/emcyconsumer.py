import struct
from ..service import Service
from .emcyevent import EMCYEvent


class EMCYConsumer(Service):
	""" EMCYConsumer

	This class is an implementation of an EMCY consumer.

	Callbacks names and arguments:
	emcy	EMCYEvent
	"""
	def __init__(self):
		Service.__init__(self)
		self._add_event("emcy")

	def attach(self, node):
		Service.attach(self, node)
		self._node.network.subscribe(0x80 + self._node.id, self.on_emcy)

	def detach(self):
		self._node.network.unsubscribe(0x80 + self._node.id, self.on_emcy)
		Service.detach(self)

	def on_emcy(self, message):
		error_code, error_register, data = struct.unpack("<HB5s", message.data)

		event = EMCYEvent(error_code, error_register, data)

		self.notify("emcy", event)

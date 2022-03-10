from ..service import Service


class SDOClient(Service):
	def attach(self, node):
		Service.attach(self, node)
		self._node.network.subscribe(0x580 + self._node.id, self.on_sdo_message)

	def detach(self):
		self._node.network.unsubscribe(0x580 + self._node.id, self.on_sdo_message)
		Service.detach(self)

	def on_sdo_message(self, message):
		""" Handler for the responses from the SDO server.
		"""
		pass

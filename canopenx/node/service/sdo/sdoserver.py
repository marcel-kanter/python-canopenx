from ..service import Service


class SDOServer(Service):
	def attach(self, node):
		Service.attach(self, node)
		self._node.network.subscribe(0x600 + self._node.id, self.on_sdo_message)

	def detach(self):
		self._node.network.unsubscribe(0x600 + self._node.id, self.on_sdo_message)
		Service.detach(self)

	def on_sdo_message(self, message):
		""" Handler for the request by the SDO client.
		"""
		pass

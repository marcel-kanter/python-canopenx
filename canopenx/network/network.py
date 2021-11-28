class Network(object):
	__slots__ = ["_bus"]

	def __init__(self):
		""" Initialises a ``Network``
		"""
		self._bus = None

	@property
	def bus(self):
		""" Returns the CAN bus this network is connected to or None if disconnected.
		"""
		return self._bus

	def connect(self, bus):
		""" Connects this network to a CAN bus. Disconnects the network first if it is already connected to a bus.
		"""
		if self.is_connected():
			self.disconnect()
		self._bus = bus

	def disconnect(self):
		""" Disconnect from the current CAN bus.
		"""
		self._bus = None

	def is_connected(self):
		""" Returns True if the network is connected to a CAN bus.
		"""
		return not self._bus is None

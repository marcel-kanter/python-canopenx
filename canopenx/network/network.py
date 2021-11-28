class Network(object):
	__slots__ = ["_bus", "_subscribers"]

	def __init__(self):
		""" Initialises a ``Network``
		"""
		self._bus = None
		self._subscribers = {}

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

	def subscribe(self, message_id, callback):
		""" Subscribe to a message id. For each message id multiple differend callbacks are allowed.
		A ValueError is raised if the callback is already registered for the specified message id.

		:param message_id: The CAN id for which the callback should be called.

		:param callback: The callback.

		:raises: ValueError
		"""
		message_id = int(message_id)
		if message_id not in self._subscribers:
			self._subscribers[message_id] = []

		if callback in self._subscribers[message_id]:
			raise ValueError("The specified callback is already registered for this message id.")

		self._subscribers[message_id].append(callback)

	def subscribed(self, message_id, callback):
		""" Returns True if the callback is registered for the specified message id.
		Returns False, if there are no callbacks registered for the message id.

		:param message_id: The CAN id for which the callback should be called.

		:param callback: The callback.
		"""
		try:
			return callback in self._subscribers[message_id]
		except KeyError:
			return False

	def unsubscribe(self, message_id, callback):
		""" Unregister the callback for the message id.
		A ValueError is raised if the callback is not in the list of callbacks (was not registered).

		:param message_id: The CAN id for which the callback should be called.

		:param callback: The callback.

		:raises: ValueError
		"""
		message_id = int(message_id)

		try:
			self._subscribers[message_id].remove(callback)
		except KeyError:
			raise ValueError("There are no callbacks registered for the specified message id.")

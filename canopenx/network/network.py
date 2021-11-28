import can


class Network(object):
	__slots__ = ["_bus", "_listeners", "_notifier", "_subscribers"]

	def __init__(self):
		""" Initialises a ``Network``
		"""
		self._bus = None
		self._subscribers = {}
		self._notifier = None
		self._listeners = [MessageListener(self)]

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
		self._notifier = can.Notifier(bus = self._bus, listeners = self._listeners, timeout = 0.1)

	def disconnect(self):
		""" Disconnect from the current CAN bus.
		"""
		if self._notifier is not None:
			self._notifier.stop()
			self._notifier = None
		self._bus = None

	def is_connected(self):
		""" Returns True if the network is connected to a CAN bus.
		"""
		return not self._bus is None

	def on_message_received(self, message):
		""" Handler for received messages. It distributes the message to all callbacks that are registered to the message id.
		"""
		try:
			for callback in self._subscribers[message.arbitration_id]:
				try:
					callback(message)
				except:
					pass
		except KeyError:
			return

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


class MessageListener(can.Listener):
	__slots__ = ["_network"]

	def __init__(self, network):
		can.Listener.__init__(self)
		self._network = network

	def on_message_received(self, message):
		self._network.on_message_received(message)

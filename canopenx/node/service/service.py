class Service(object):
	""" Service

	This class is the base class for all services of a node.

	It has a callback mechanism that supports multiple events and multiple callbacks for each event.
	"""

	__slots__ = ["_callbacks", "_node"]

	def __init__(self):
		self._node = None
		self._callbacks = {}

	def _add_event(self, event):
		""" Adds an event to this service.
		Raises KeyError if the event is already added to the service.

		:param event: The name of the event.

		:raises: ValueError
		"""
		if event in self._callbacks:
			raise KeyError("This event is already added to the service.")

		self._callbacks[event] = []

	def _remove_event(self, event):
		""" Removes an event from the service.
		Raises KeyError if the event is not found.

		:param event: The name of the event.

		:raises: KeyError
		"""
		del self._callbacks[event]

	def add_callback(self, event, callback):
		""" Adds the given callback for the event.
		Raises TypeError if the callback is not callable.
		Raises KeyError if the event is not supported/found.

		:param event: The name of the event

		:param callback: The callback function. Must be callable

		:raises: TypeError, KeyError
		"""
		if not callable(callback):
			raise TypeError()

		self._callbacks[event].append(callback)

	def attach(self, node):
		""" Attach handler.

		Must be called when the node gets attached to the network.
		"""
		if self.is_attached():
			self.detach()
		self._node = node

	def detach(self):
		""" Detach handler.

		Must be called when the node gets detached from the network.
		"""
		self._node = None

	def has_callback(self, event, callback):
		""" Returns True if the specified callback has been added to the event.
		"""
		return callback in self._callbacks[event]

	def has_event(self, event):
		""" Returns True if the specified event has been added to the service.
		"""
		return event in self._callbacks

	def is_attached(self):
		""" Returns True if the service is attached.
		"""
		return self._node is not None

	@property
	def node(self):
		""" Returns the node this service belongs to or None if the service is not attached.
		"""
		return self._node

	def notify(self, event, *args):
		""" Call the callbacks for the given event.
		If a callback raises an exception, it will be ignored.
		Raises KeyError if the event has not been added to the service.

		:param event: The name of the event

		:param args: A list of arguments to pass to the callback

		:raises: KeyError
		"""
		for callback in self._callbacks[event]:
			try:
				callback(*args)
			except Exception:
				pass

	def remove_callback(self, event, callback):
		""" Removes the callback for the event.
		Raises KeyError if the event is not supported/found.
		Raises ValueError if the callback was not found.

		:param event: The name of the event

		:param callback: The callback function. Must be callable

		:raises: KeyError, ValueError
		"""
		self._callbacks[event].remove(callback)

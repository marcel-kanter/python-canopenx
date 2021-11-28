import can


class Network(object):
	__slots__ = ["_bus", "_listeners", "_nodes_id", "_nodes_name", "_notifier", "_subscribers"]

	def __contains__(self, key):
		""" Returns True if the network contains a node with the specified node id

		:param key: The node id to look for

		:returns: True if a node is in the network with the given node id
		"""
		try:
			self[key]
		except:
			return False
		else:
			return True

	def __delitem__(self, key):
		""" Removes a node identified by a node id from the network.
		Raises KeyError if there is no node in the network with the given node id.

		:param key: The name or identifier of the node to remove

		:raises: KeyError
		"""
		node = self[key]

		del self._nodes_id[node.id]
		if node.name is not None:
			del self._nodes_name[node.name]

	def __getitem__(self, key):
		""" Returns the node identified by the node id.
		Raises KeyError if there is no node in the network with the given node id.

		:param key: The node id to look for

		:returns: A ``Node`` object

		:raises: KeyError
		"""
		try:
			return self._nodes_id[key]
		except KeyError:
			return self._nodes_name[key]

	def __init__(self):
		""" Initialises a ``Network``
		"""
		self._bus = None
		self._subscribers = {}
		self._nodes_id = {}
		self._nodes_name = {}
		self._notifier = None
		self._listeners = [MessageListener(self)]

	def __iter__(self):
		""" Returns an iterator over all nodes in the network.
		"""
		return iter(self._nodes_id.values())

	def __len__(self):
		""" Returns the number of nodes in the network.
		"""
		return len(self._nodes_id)

	def add(self, node):
		""" Adds a node to the network. It may be accessed later by the node id.
		Raises ValueError if a node with the node id is already in the network.

		:param node: The node to add

		:raises: ValueError
		"""
		if node.id in self._nodes_id:
			raise ValueError("A node with this id is already in the network.")
		if node.name is not None and node.name in self._nodes_name:
			raise ValueError("A node with this name is already in the network.")

		self._nodes_id[node.id] = node
		if node.name is not None:
			self._nodes_name[node.name] = node

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

	def send(self, message):
		""" Sends a CAN message on the CAN bus.
		Raises RuntimeError if the network is not connected to a bus.

		:param message: The message to send.

		:raises: RuntimeError
		"""
		if not self.is_connected():
			raise RuntimeError("The network is not connected to a CAN bus.")

		self._bus.send(message)

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

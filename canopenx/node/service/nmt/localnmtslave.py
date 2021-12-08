from .nmtservice import NMTService


class LocalNMTSlave(NMTService):
	def __init__(self):
		NMTService.__init__(self)

	@property
	def state(self):
		return self._state

	@state.setter
	def state(self, value):
		"""
		:param value: The new NMT state. Must be in range 0 .. 127.

		:raises: ValueError
		"""
		if value < 0 or value > 127:
			raise ValueError("The specified value is out of range 0 .. 127.")
		self._state = value

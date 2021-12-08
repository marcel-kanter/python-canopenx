from ..service import Service
from canopenx.nmt.states import INITIALIZING


class NMTService(Service):
	__slots__ = ["_state"]

	def __init__(self):
		Service.__init__(self)
		self._state = INITIALIZING

	@property
	def state(self):
		return self._state

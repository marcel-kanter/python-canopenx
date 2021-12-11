class EMCYEvent(object):

	__slots__ = ["error_code", "error_register", "data"]

	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self is other or (self.error_code == other.error_code and self.error_register == other.error_register and self.data == other.data)

	def __init__(self, error_code, error_register, data):
		self.error_code = error_code
		self.error_register = error_register
		self.data = data

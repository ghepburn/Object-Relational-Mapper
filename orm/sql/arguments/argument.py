

class Argument:
	sql = None

	@classmethod
	def get_name(cls):
		return cls.__name__.lower()

	def apply(self, sql, values):
		pass
	
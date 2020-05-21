

class Query_Data:
	def __init__(self, *args):
		self._data = []
		for arg in args:
			self._data.append(arg)

	@property
	def data(self):
		return self._data

	def first(self):
		return self.data[0]

	def last(self):
		return self.data[-1]
	
	def __repr__(self):
		return f"<Data Container {self.data}>"

	def __str__(self):
		return f"{self.data}"

	
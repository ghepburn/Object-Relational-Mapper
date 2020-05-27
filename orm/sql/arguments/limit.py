from.argument import Argument
from ..statements import LIMIT_SQL

class Limit(Argument):
	sql = LIMIT_SQL

	def __init__(self, value):
		self.value = value

	def get_sql(self):
		return self.sql.format(number=self.value)
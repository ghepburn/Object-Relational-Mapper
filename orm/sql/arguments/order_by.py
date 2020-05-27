from.argument import Argument
from ..statements import ORDERBY_ASC_SQL, ORDERBY_DESC_SQL

class Order_By(Argument):
	sql = ORDERBY_ASC_SQL

	def __init__(self, field):
		self.field = field
		if field[0] == "-":
			self.sql = ORDERBY_DESC_SQL
			self.field = field[1:]


	def get_sql(self):
		return self.sql.format(field=self.field)
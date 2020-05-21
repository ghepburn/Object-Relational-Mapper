from .sql import COLUMN_CREATE_SQL, FOREIGNKEY_CREATE_SQL

POSTGRES_TYPE_MAP = {
	str:'VARCHAR',
	int:'INTEGER'
}

class Column:
	def __init__(self, python_type):
		self.type = python_type

	@property
	def sql_type(self):
		return POSTGRES_TYPE_MAP[self.type]

	def _get_create_sql(self, name):
		sql = COLUMN_CREATE_SQL.format(name=name, type=self.sql_type)
		return sql	

class ForeignKey:
	def __init__(self, table):
		self.referenced_table = table
		self.referenced_table_name = self.referenced_table.__name__.lower()

	@property
	def sql_type(self):
		return POSTGRES_TYPE_MAP[int]

	def _get_create_sql(self, name):
		sql = COLUMN_CREATE_SQL.format(name=name, type=self.sql_type, table=self.referenced_table_name, table_name="id")
		print(sql)
		return sql
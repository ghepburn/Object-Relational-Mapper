from . import statements

POSTGRES_TYPE_MAP = {
	str:'VARCHAR',
	int:'INTEGER',
	'ser':'SERIAL'
}

class Column:
	type_mapper = POSTGRES_TYPE_MAP
	primary_key = False
	foreign_key = False

	CREATE_SQL = statements.COLUMN_CREATE_SQL
	CREATE_PK_SQL = statements.COLUMN_PK_CREATE_SQL

	def __init__(self, python_type, *args, **kwargs):
		self._type = python_type
		self.default = None

		if "primary_key" in args:
			self.primary_key = True
			self.CREATE_SQL = self.CREATE_PK_SQL

		if "default" in kwargs:
			self.default = kwargs["default"]

	@property
	def sql_type(self):
		return self.type_mapper[self._type]

	def is_primary_key(self):
		return self.primary_key

	def _get_create_sql(self, name):
		sql_type = self.sql_type
		return self.CREATE_SQL.format(name=name, type=sql_type)
			

class ForeignKey(Column):
	CREATE_SQL = statements.FOREIGNKEY_CREATE_SQL

	def __init__(self, table):
		self._table = table
		self._table_name = self._table.get_name()
		self.foreign_key = True

	def is_foreign_key(self):
		return self.foreign_key

	def get_primary_key(self):
		pk = self._table.get_primary_key()
		return pk

	@property
	def sql_type(self):
		return self.type_mapper[int]	

	def _get_create_sql(self, name):
		return self.CREATE_SQL.format(name=name, type=self.sql_type, table=self._table_name, field=self._table.get_primary_key())
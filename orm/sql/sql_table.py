import inspect

from .arguments import Filter
from . import statements
from .sql_columns import Column, ForeignKey

class SQL_Table():
	acceptable_columns = [Column, ForeignKey]
	acceptable_arguments = [Filter]

	CREATE_SQL = statements.TABLE_CREATE_SQL
	SELECT_SQL = statements.TABLE_SELECT_SQL
	SELECT_WHERE_SQL = statements.TABLE_SELECT_WHERE_SQL
	DROP_SQL = statements.TABLE_DROP_SQL
	INSERT_SQL = statements.TABLE_INSERT_SQL
	UPDATE_SQL = statements.TABLE_UPDATE_SQL
	DELETE_SQL = statements.INSTANCE_DELETE_SQL

	@classmethod
	def get_name(cls):
		return cls.__name__.lower()

	@classmethod
	def get_fields(cls):
		fields = {}
		for name, column in inspect.getmembers(cls):
			if column.__class__ in cls.acceptable_columns:
				fields[name] = column
		return fields

	@classmethod
	def is_primary_key(cls):
		pk = cls.get_primary_key()
		if pk != None:
			return True
		else:
			return False

	@classmethod
	def get_primary_key(cls):
		pk = None
		for name, column in inspect.getmembers(cls):
			if column.__class__ in cls.acceptable_columns:
				if column.is_primary_key():
					pk = name
		return pk

	@classmethod
	def _set_default_primary_key(cls):
		cls.id = Column('ser', "primary_key")

	@classmethod
	def get_foreign_keys(cls):
		foreign_keys = {}
		for name, column in inspect.getmembers(cls):
			if column.__class__ in cls.acceptable_columns:
				if isinstance(column, ForeignKey):
					foreign_keys[name] = column
		return foreign_keys

	@classmethod
	def _convert_to_string(self, sequence):
		if type(sequence) == str or type(sequence) == int:
			return sequence
		else:
			return ", ".join(sequence)

	@classmethod
	def _get_sql_fields(cls):
		sql_fields = []
		for name, field in cls.get_fields().items():
			sql_fields.append(field._get_create_sql(name))
		return cls._convert_to_string(sql_fields)

	@classmethod
	def _get_create_sql(cls):
		if not cls.is_primary_key():
			cls._set_default_primary_key()
		fields = cls._get_sql_fields()
		return cls.CREATE_SQL.format(table=cls.get_name(), fields=fields)

	@classmethod
	def _get_select_sql(cls, fields=["*"]):
		fields = cls._convert_to_string(fields)
		return cls.SELECT_SQL.format(fields=fields, table=cls.get_name())

	@classmethod
	def _get_select_where_sql(cls, filters, fields=["*"]):
		fields = cls._convert_to_string(fields)
		filters = cls._convert_to_string(filters)
		table = cls.get_name()
		return cls.SELECT_WHERE_SQL.format(fields=fields, table=cls.get_name(), filters=filters)

	@classmethod
	def _get_insert_sql(cls, fields="*"):
		if fields == "*":
			fields = cls.get_fields().keys()
		placeholders = cls._convert_to_string(["%s"] * len(fields))
		fields = cls._convert_to_string(fields)
		pk = cls.get_primary_key()
		sql = cls.INSERT_SQL.format(table=cls.get_name(), fields=fields, placeholders=placeholders, pk=pk)
		return sql

	@classmethod
	def _get_update_sql(cls, field):
		sql = cls.UPDATE_SQL.format(table=cls.get_name(), field=field, pk=cls.get_primary_key())
		return sql

	@classmethod
	def _get_drop_table_sql(cls, table=None):
		if table==None:
			table=cls.get_name()
		return cls.DROP_SQL.format(table=table)

	@classmethod
	def _get_delete_sql(cls, field):

		filters = field + "=%s"
		
		sql = cls.DELETE_SQL.format(table=cls.get_name(), filters=filters)
		return sql

	def __repr__(self):
		return f"<{self.__class__.__name__}>"

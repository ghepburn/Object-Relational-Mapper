import inspect

from .table_contents import Column, ForeignKey
from .sql import TABLE_SELECT_SQL, TABLE_CREATE_SQL, TABLE_INSERT_SQL, TABLE_SELECT_WHERE_SQL, TABLE_DROP_SQL, INSTANCE_DELETE_SQL, TABLE_UPDATE_SQL
from .observer import Subject

class Table(Subject):
	def __init__(self, **kwargs):
		self._data = kwargs
		super().__init__()

	def __getattribute__(self, key):
		_data = object.__getattribute__(self, '_data')
		if key in _data:
			return _data[key]
		return object.__getattribute__(self, key)

	def __setattr__(self, key, value):
		if key == "_data" or key == "subscribers":
			object.__setattr__(self, key, value)
		else:
			_data = self._data
			_data[key] = value

			fields = self.__class__.get_fields()
			if key in fields:
				sql, values = self._get_update_sql(key, _data[key])
				self.notify_subscribers(sql, values)

	@classmethod
	def get_name(cls):
		return cls.__name__.lower()

	@classmethod
	def get_fields(cls):
		# fields = {"id":Column}
		fields = {}
		for name, field in inspect.getmembers(cls):
			if isinstance(field, Column) or isinstance(field, ForeignKey):
				fields[name] = field
		return fields

	@classmethod
	def get_sql_fields(cls):
		sql_fields = ["id SERIAL PRIMARY KEY"]
		fields = cls.get_fields()
		print(fields)
		for key, value in fields.items():
			sql_fields.append(value._get_create_sql(key))
		print(sql_fields)
		return ", ".join(sql_fields)

	def field_exists(self, field):
		existing_fields = self.__class__.get_fields()
		if field in existing_fields:
			return True
		else:
			return False

	@classmethod
	def _get_create_sql(cls):
		name = cls.get_name()
		fields = cls.get_sql_fields()
		sql = TABLE_CREATE_SQL.format(name=name, fields=fields)
		return sql

	def _get_insert_sql(self):
		name = self.__class__.get_name()
		existing_fields = self.__class__.get_fields() 

		fields = []
		values = []
		placeholders = []

		for key, value in self._data.items():
			if key in existing_fields:
				print(key, value)
				if isinstance(existing_fields[key], ForeignKey):
					value = value.id
				fields.append(key)
				values.append(value)
				placeholders.append("%s")

		placeholders = ", ".join(placeholders)
		fields = ", ".join(fields)

		sql = TABLE_INSERT_SQL.format(name=name, fields=fields, placeholders=placeholders)
		return sql, values

	def _get_update_sql(self, key, value):
		name = self.__class__.get_name()
		instance_id = self.id
		existing_fields = self.__class__.get_fields()
		if self.field_exists(key):

			
			values = [value, instance_id]
			sql = TABLE_UPDATE_SQL.format(name=name, field=key, filter="id")
			return sql, values

	@classmethod
	def _get_select_sql(cls, **kwargs):
		name = cls.get_name()
		fields = list(cls.get_fields().keys())
		str_fields = ", ".join(fields)
		sql = TABLE_SELECT_SQL.format(fields=str_fields, name=name)
		return sql, fields

	@classmethod
	def _get_select_where_sql(cls, **kwargs):
		name = cls.get_name()
		fields = list(cls.get_fields().keys())
		
		filters = []
		values = []

		# equals arguments
		for key, value in kwargs.items():
			if key == "filters":
				for filter_statement in value:
					filter_field = filter_statement[0]
					filter_operator = filter_statement[1]
					filter_value = filter_statement[2]
					print(filter_field, filter_operator, filter_value)
					filters.append(filter_field + " " + filter_operator + " " + "%s")
					values.append(filter_value)
			else:
				filters.append(key + " = %s")
				values.append(value)

		str_fields = ", ".join(fields)
		filters = " and ".join(filters)
		
		sql = TABLE_SELECT_WHERE_SQL.format(fields=str_fields, name=name, filters=filters)
		print(sql)
		return sql, fields, values

	@classmethod
	def _get_drop_table_sql(cls):
		name = cls.get_name()
		sql = TABLE_DROP_SQL.format(name=name)
		return sql

	def _get_delete_sql(self):
		table_name = self.__class__.get_name()
		field = "id"
		value = str(self.id)
		placeholder = "%s"
		sql = INSTANCE_DELETE_SQL.format(table=table_name, field=field, placeholder=placeholder)
		return sql, value

	def __repr__(self):
		return f"<{self.__class__.__name__}>"

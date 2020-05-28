from .sql import SQL_Table
from .observer import Subject
from .query import Query

class Table(SQL_Table):

	def __init__(self, mapped=False, **kwargs):
		super().__init__()
		self._data = kwargs
		if not mapped:
			self._insert()

	def __getattribute__(self, key):
		_data = object.__getattribute__(self, '_data')
		if key in _data:
			return _data[key]
		return object.__getattribute__(self, key)

	def __setattr__(self, key, value, update=True):
		if key == "_data":
			object.__setattr__(self, key, value)
		else:
			if self.valid_field(key):
				_data = self._data
				_data[key] = value
				if update:
					self._update(key, value)
	
	def valid_field(self, field):
		fields = self.__class__.get_fields()
		if field in fields:
			return True
		else:
			return False

	def _insert(self):
		fk = self.get_foreign_keys()
		fields = list(self._data.keys())
		values = list(self._data.values())

		for key in fk:
			idx = fields.index(key)
			fk_table = values[idx]
			pk = fk_table.get_primary_key()
			values[idx] = values[idx].__getattribute__(pk)

		sql = self._get_insert_sql(fields)
		data = self.notify_subscribers(sql, values)[0]

		# update instance data
		pk = list(data.keys())[0]
		if pk not in self._data:
			value = data[pk]
			self.__setattr__(pk, value, update=False)

	def _update(self, field, value):
		if field in self.get_foreign_keys().keys():
			pk = self.get_foreign_keys()[field].get_primary_key()
			value = value.__getattribute__(pk)
		sql = self._get_update_sql(field)
		pk = self._data[self.get_primary_key()]
		values = [value, pk]
		self.notify_subscribers(sql, values)

	@classmethod
	def query(cls):
		return Query(cls)

	@classmethod
	def remove(cls, instance):
		pk = instance.get_primary_key()
		values = []
		
		values.append(instance.__getattribute__(pk))
		sql = cls._get_delete_sql(pk)
		cls.notify_subscribers(sql, values)

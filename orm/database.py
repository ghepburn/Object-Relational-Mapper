import psycopg2
import inspect

from .table import Table
from .table_contents import Column, ForeignKey
from .connection import Connection
from .query import Query
from .sql import GET_ALL_TABLES_SQL



class Database(Connection):
	def __init__(self, host, database, user, password):
		super().__init__(host, database, user, password)

	@property
	def tables(self):
		tables = self._execute(GET_ALL_TABLES_SQL)
		tables_list = [", ".join(x) for x in tables]
		return tables_list

	def table_exists(self, table):
		tables = self.tables
		table_names = [table.__name__, table.__name__.lower(), table.__name__.upper()]
		for table in table_names:
			if table in tables:
				return True
		return False


	# Create ----------------------


	def create(self, table):
		if not self.table_exists(table):
			sql = table._get_create_sql()
			self._execute(sql)
		else:
			# raise error
			pass


	# Read ----------------------


	def query(self, table, **kwargs):
		return Query(self, table, **kwargs)


	# Update ----------------------


	def add(self, instance):
		sql, values = instance._get_insert_sql()
		data = self._execute(sql, values)
		instance.id = int(str(data)[2])
		self._manual_connect(instance)

	def _manual_connect(self, instance):
		instance.subscribe(self)
		
	def _notify(self, *args):
		self._execute(*args)


	# Delete ----------------------


	def delete(self, instance):
		sql, values = instance._get_delete_sql()
		self._execute(sql, values)

	def drop_table(self, table):
		sql = table._get_drop_table_sql()
		self._execute(sql)


	# Close ----------------------


	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

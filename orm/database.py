import psycopg2
import inspect

from .table import Table
from .connection import Connection
from .query import Query
from .sql import statements, SQL_Table
from .observer.subject import Subject



class Database(Connection):

	TABLES_SQL = statements.GET_ALL_TABLES_SQL
	
	def __init__(self, host, database, user, password):
		super().__init__(host, database, user, password)

	@property
	def model(self):
		class Model(Table, Subject):
			subscribers = [self]
		return Model

	@property
	def tables(self):
		tables = self._execute(self.TABLES_SQL)
		tables_list = [", ".join(x.values()) for x in tables]
		return tables_list

	def table_exists(self, table):
		tables = self.tables
		if table.get_name() in tables:
			return True
		else:
			return False


	# Create ----------------------


	def create(self, table):
		if not self.table_exists(table):
			sql = table._get_create_sql()
			self._execute(sql)
			# table.subscribe(self)

		
	def _notify(self, *args):
		return self._execute(*args)


	# Delete ----------------------

	def drop_table(self, table):
		if type(table) == str:
			sql = SQL_Table._get_drop_table_sql(table=table)
		else:
			sql = table._get_drop_table_sql()
		self._execute(sql)

	# SQL ----------------------
	def sql(self, sql):
		return self._execute(sql)


	# Close ----------------------


	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

from .query_data import Query_Data
from .sql import SQL_Factory

class Query:
	def __init__(self, db, table, **kwargs):
		self.db = db
		self.table = table
		self.sql_factory = SQL_Factory()
		self.sql_arguments = []

		for key, value in kwargs.items():
			self.sql_arguments.append(self.sql_factory.get_sql(key, value))

	def all(self, **kwargs):
		
		# currently ignores all arguments

		sql, fields = self.table._get_select_sql(**kwargs)
		return self.process_query(sql, fields)

	def get(self, **kwargs):

		# takes only equals arguments

		if not kwargs:
			sql, fields = self.table._get_select_sql()
			values = None
		else:
			sql, fields, values = self.table._get_select_where_sql(**kwargs)
		
		return self.process_query(sql, fields, values)

	def filter(self, *args):
		acceptable_operators = ["=", ">", "<"]
		filters = []
		for arg in args:
			str_filter = arg.split()
			if len(str_filter) == 3:
				filters.append(str_filter)
			else:
				for operator in acceptable_operators:
					if operator in arg:
						str_filter = arg.split(operator)
						str_filter.append(operator)
						str_filter[1], str_filter[2] = str_filter[2], str_filter[1]
						filters.append(str_filter)
					else:
						print("Incorrect Filter Argument")

		sql, fields, values = self.table._get_select_where_sql(filters=filters)
		
		return self.process_query(sql, fields, values)
		
	def process_query(self, sql, fields=None, values=None):
		# add additional arguments
		for arg in self.sql_arguments:
			sql += arg

		# process
		raw_data = self.db._execute(sql, values)
		
		# standardize format
		query_data = self.standardize(raw_data, fields)
		
		return query_data

	def standardize(self, raw_data, fields):
		# map rows to dictionaries
		data = []
		for row in raw_data:
			data_set = dict(zip(fields, row))
			data.append(data_set)

		# instantiate dictionaries as objects
		object_list = []
		for data_set in data:
			new_object = self.table(**data_set)
			self.db._manual_connect(new_object)
			object_list.append(new_object)

		# return data representation object
		return Query_Data(*object_list)
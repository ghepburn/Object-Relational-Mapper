from .query_data import Query_Data
from .sql import Order_By, Limit, Filter
from collections import deque

class Query:

	package_data = Query_Data
	postprocess_arguments = [Order_By, Limit]

	def __init__(self, table):
		self.table = table
		self.sql_filter = Filter(self.table)
		self.argument_queue = deque()

	def all(self, columns="*", **kwargs):
		
		self._process_args(**kwargs)

		sql = self.table._get_select_sql(fields=columns)
		
		return self._process_query(sql)

	def get(self, columns="*", **kwargs):

		self.sql_filter.input(**kwargs)
		filters, values = self.sql_filter.get()

		self._process_args(**kwargs)

		sql = self.table._get_select_where_sql(fields=columns, filters=filters)

		return self._process_query(sql, values=values)

	def filter(self, sql_filter, columns="*", **kwargs):

		self.sql_filter.input(sql_filter, **kwargs)
		filters, values = self.sql_filter.get()

		self._process_args(**kwargs)
		sql = self.table._get_select_where_sql(filters=filters, fields=columns)
		return self._process_query(sql, values)

	def _process_args(self, **kwargs):

		for arg in self.postprocess_arguments:
			print(arg.get_name())
			if arg.get_name() in kwargs:
				requested_arg = arg(kwargs[arg.get_name()])
				self.argument_queue.append(requested_arg)

	def _process_query(self, sql, values=None):

		# add additional arguments
		while len(self.argument_queue) > 0:
			arg = self.argument_queue.popleft()
			sql += arg.get_sql()
			print(sql)

		if values != None and len(values) > 0:
			data = self.table.notify_subscribers(sql, values)
		else:
			data = self.table.notify_subscribers(sql)

		packaged_data = self._standardize(data)
		
		return packaged_data

	def _standardize(self, data):
		all_data = []
		# instantiate dictionaries as objects
		for response in data:
			object_list = []
			for row in response:
				new_object = self.table(mapped=True, **row)
				object_list.append(new_object)
			all_data.append(self.package_data(*object_list))
		
		# return data representation object
		if len(all_data) == 1:
			return all_data[0]
		else:
			return all_data
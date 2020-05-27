from .argument import Argument
from ..statements import FIELD_FILTER_SQL

class Filter(Argument):

	acceptable_operators = ["=", ">", "<"]
	default_operator = "="
	default_placeholder = "%s"
	sql = FIELD_FILTER_SQL

	def __init__(self, table):
		self._fields = table.get_fields().keys()
		self._filters = []
		self._values = []

	def input(self, strings=None, **kwargs):
		if strings:
			self._process_strings(strings)
		if len(kwargs)>0:
			self._process_kwargs(**kwargs)

	def _process_strings(self, string):
		if type(string) == list:
			for arg in strings:
				field, operator, value = self._parse_filter_string(arg)
		else:
			field, operator, value = self._parse_filter_string(string)
		self._set(field, operator, value)

	def _process_kwargs(self, **kwargs):
		for arg in kwargs:
			field = arg
			operator = self.default_operator
			value = kwargs[arg]
			self._set(field, operator, value)

	def _set(self, field, operator, value):
		if self._valid_field(field):
			arg_sql = self.sql.format(field=field, operator=operator, placeholder=self.default_placeholder) 
			self._filters.append(arg_sql)
			self._values.append(value)

	def _parse_filter_string(self, string_statement):
		if len(string_statement.split()) == 3:
			field, operator, value = string_statement.split()
		else:
			for op in self.acceptable_operators:
				if op in string_statement:
					field, value = string_statement.split(op)
					operator = op
		try:
			value = int(value)
		except:
			pass
		return field, operator, value

	def _valid_field(self, field):
		if field in self._fields:
			return True
		else:
			return False

	def get(self):
		filters = ", ".join(self._filters)
		values = self._values
		return filters, values
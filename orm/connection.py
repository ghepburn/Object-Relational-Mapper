import psycopg2

from .observer import Subscriber
from .query_data import Query_Data

class Connection(Subscriber):

	data_package = Query_Data
	
	def __init__(self, host, database, user, password):
		self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

	def check_transaction_status(self):
		if self.conn.get_transaction_status() in [3]:
			self.conn.rollback()

	def _execute(self, sql, values=None):
		self.check_transaction_status()
		cur = self.conn.cursor()
		
		if values:
			cur.execute(sql, values)
		else:
			cur.execute(sql)
		try:
			values = cur.fetchall()
			fields = [i.name for i in cur.description]
			cur.close()
			data = self.standardize(values, fields)
			return data
		except:
			cur.close()

	def standardize(self, raw_values, fields):
		
		data = []
		for row in raw_values:
			data_set = dict(zip(fields, row))
			data.append(data_set)
		if len(data) == 1:
			data = data[0]
		return data
		



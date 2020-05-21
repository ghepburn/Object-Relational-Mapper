import psycopg2

from .observer import Subscriber

class Connection(Subscriber):
	def __init__(self, host, database, user, password):
		self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

	def check_transaction_status(self):
		if self.conn.get_transaction_status() == 3:
			self.conn.rollback()

	def _execute(self, sql, values=None):
		self.check_transaction_status()
		cur = self.conn.cursor()
		
		if values:
			cur.execute(sql, values)
		else:
			cur.execute(sql)
		try:
			data = cur.fetchall()
			cur.close()
			return data
		except:
			cur.close()
		



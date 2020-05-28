import pytest
import psycopg2
from tests import db, Database, Table, Column, ForeignKey


class Dog(db.model):
	pk = Column(int, "primary_key")
	name = Column(str)

class Cat(db.model):
	name = Column(str)
	friend = ForeignKey(Dog)

class Test_Database:

	def test_connection(self):
		assert isinstance(db.conn, psycopg2.extensions.connection)

	def test_execute(self):

		ex1 = db._execute("SELECT * FROM products")
		ex2 = db._execute("SELECT * FROM products WHERE name=%s", ["hammer"])

		assert len(ex1) > 1
		assert ex2 == [{'id': 1, 'name': 'hammer', 'price': 10}]


	def test_create(self):

		db.create(Dog)
		db.create(Cat)

		assert Dog._get_create_sql() == "CREATE TABLE dog (name VARCHAR, pk INTEGER PRIMARY KEY)"
		assert Cat._get_create_sql() == "CREATE TABLE cat (friend INTEGER REFERENCES dog(pk), id SERIAL PRIMARY KEY, name VARCHAR)"


	def test_get_tables(self):
		tables = db.tables

		assert len(tables) > 3
		assert 'dog' in tables

	def test_table_exists(self):

		assert db.table_exists(Dog) == True

	def test_drop_table(self):
		
		db.drop_table(Cat)
		db.drop_table(Dog)

		tables = db.tables

		assert 'cat' not in tables
		assert 'dog' not in tables

	def test_close_db(self):

		db.close()
		assert db.conn.closed == 1

import pytest
import psycopg2
# import os
# import sys
# sys.path.append("C:\\Users\\Greg\\Python_Projects\\WebDevelopment\\orm")

# password = os.environ.get("GREGDB_PASSWORD")

from tests import db, Database, Table, Column, ForeignKey


class Dog(Table):
	name = Column(str)

class Cat(Table):
	name = Column(str)
	friend = ForeignKey(Dog)


class Test_Database:

	def test_connection(self):
		assert isinstance(db.conn, psycopg2.extensions.connection)

	def test_basic_column(self):	

		assert Dog.name.type == str
		assert Dog.name.sql_type == "VARCHAR"

	def test_create(self):

		db.create(Dog)
		db.create(Cat)

		assert Dog._get_create_sql() == "CREATE TABLE dog (id SERIAL PRIMARY KEY, name VARCHAR)"
		assert Cat._get_create_sql() == "CREATE TABLE cat (id SERIAL PRIMARY KEY, friend INTEGER, name VARCHAR)"

		for table in ['dog', 'cat']:
			assert table in db.tables

	def test_add(self):

		dug = Dog(name="Dug")
		assert dug._get_insert_sql() == ("INSERT INTO dog (name) VALUES (%s) RETURNING (id)", ['Dug'])
		
		db.add(dug)
		assert dug.id == 1

	def test_instances(self):

		henry = Dog(name="Henry")
		db.add(henry)
		assert henry.id == 2

		james = Dog(name="James")
		db.add(james)
		assert james.id == 3

		assert henry.name == "Henry"


	def test_drop_table(self):
		
		class Frog(Table):
			name = Column(str)

		db.create(Frog)

		assert 'frog' in db.tables

		db.drop_table(Frog)

		assert Frog._get_drop_table_sql() == "DROP TABLE frog"
		assert 'frog' not in db.tables

	def test_delete_instance(self):
		
		bruce = Dog(name='Bruce')
		db.add(bruce)

		db.delete(bruce)

		sql, value = bruce._get_delete_sql()
		assert sql == "DELETE FROM dog WHERE id=%s"
		assert value == str(bruce.id)

	def test_foreign_keys(self):

		tom = Dog(name="Tom")
		db.add(tom)
		sam = Cat(name='Sam', friend=tom)

		assert sam.friend == tom
		sql, values = sam._get_insert_sql() 
		assert sql == "INSERT INTO cat (name, friend) VALUES (%s, %s) RETURNING (id)"
		assert values == ['Sam', tom.id]
		
		db.add(sam)


	def test_close_db(self):
		db.close()
		assert db.conn.closed == 1

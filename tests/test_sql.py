import pytest
from tests import orm
SELECT_SQL =  orm.statements.TABLE_SELECT_SQL
sql_table = orm.sql.SQL_Table
Column = orm.Column
Foreign_Key = orm.ForeignKey


class table1(sql_table):
	name = Column(str)
	age = Column(int)


class Test_Table:
	
	def test_fields(self):
	
		fields = table1.get_fields()   
		assert len(fields) == 2

	def test_is_primary_key(self):
		assert table1.is_primary_key() == False

	def test_set_default_primary_key(self):

		table1._set_default_primary_key()
		assert table1.is_primary_key() == True
		assert table1.get_primary_key() == 'id'

	def test_foreignkey(self):

		assert len(table1.get_foreign_keys().keys()) == 0

	def test_sql_fields(self):
		fields = table1._get_sql_fields()
		assert fields == "age INTEGER, id SERIAL PRIMARY KEY, name VARCHAR"
	
	def test_create_sql(self):

		class new_table(sql_table):
			pass

		sql = table1._get_create_sql()
		sql_newtable = new_table._get_create_sql()
		
		assert sql == "CREATE TABLE table1 (age INTEGER, id SERIAL PRIMARY KEY, name VARCHAR)"
		assert sql_newtable == "CREATE TABLE new_table (id SERIAL PRIMARY KEY)"

	def test_select_sql(self):
		sql_all = table1._get_select_sql()
		sql_name = table1._get_select_sql(fields=["name"])
		
		assert sql_all == "SELECT * FROM table1"
		assert sql_name == "SELECT name FROM table1"

	def test_select_where_sql(self):

		gt = table1._get_select_where_sql(filters=["id>3"])
		multiple = table1._get_select_where_sql(filters=["name=Greg", "age>15"])

		assert gt == "SELECT * FROM table1 WHERE id>3"
		assert multiple == "SELECT * FROM table1 WHERE name=Greg, age>15"


	def test_insert_sql(self):

		sql = table1._get_insert_sql()
		assert sql == "INSERT INTO table1 (age, id, name) VALUES (%s, %s, %s) RETURNING (id)"
		
	def test_update_sql(self):
		sql = table1._get_update_sql('name')

		assert sql == "UPDATE table1 SET name=%s WHERE id=%s"
		
	def test_drop_sql(self):
		sql = table1._get_drop_table_sql()

		assert sql == "DROP TABLE table1"

	def test_delete_sql(self):
		sql_one = table1._get_delete_sql("name")
		
		assert sql_one == "DELETE FROM table1 WHERE name=%s"
		
class Test_Column:
	
	def test_sql_type(self):
		assert table1.name.sql_type == 'VARCHAR'
		assert table1.age.sql_type == 'INTEGER'

	def test_is_primary_key(self):

		assert table1.name.is_primary_key() == False
		assert table1.age.is_primary_key() == False
		assert table1.id.is_primary_key() == True

	def test_create_sql(self):
		age_sql = table1.age._get_create_sql("age")
		name_sql = table1.name._get_create_sql("name")

		assert name_sql == "name VARCHAR"
		assert age_sql == "age INTEGER"

	def test_primary_key(self):
		class table2(sql_table):
			pk = Column(int, 'primary_key')
			name = Column(str)

		assert table2.pk.is_primary_key() == True
		assert table2.pk._get_create_sql("pk") == "pk INTEGER PRIMARY KEY"
		assert table2.name._get_create_sql("name") == "name VARCHAR"


class table3:
	pk = Column(int, "primary_key")
	friend = Foreign_Key(table1)

class Test_Foreign_Key:

	def test_sql_type(self):
		assert table3.friend.sql_type == "INTEGER"

	def test_is_primary_key(self):
		assert table3.friend.is_primary_key() == False

	def test_is_foreign_key(self):
		assert table3.friend.is_foreign_key() == True

	def test_create_sql(self):
		assert table3.friend._get_create_sql("friend") == "friend INTEGER REFERENCES table1(id)"


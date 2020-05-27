import pytest
from tests import orm, db

Table = orm.Table
Column = orm.Column
Query = orm.Query


class Test_Table_Instance:

	def test_instance(self):

		global greg, mandy, User

		class User(Table):
			pk = Column(int, "primary_key")
			name = Column(str)

		greg = User(pk=1, name="Greg")

		class Person(Table):
			name = Column(str)
			age = Column(int)	

		mandy = Person(name="Mandy", age=22)


	def test_getter(self):
		name = greg.name
		pk = greg.pk
		data = greg._data

		assert name == "Greg"
		assert pk == 1
		assert data == {"pk":1, "name":"Greg"}

	def test_setter(self):

		greg.name = "Not Greg"
		greg.age = 25

		assert greg.name == "Not Greg"
		assert "age" not in greg._data.keys()

		greg.name = "Greg"

	def test_primary_key(self):

		greg_pk = greg.get_primary_key()
		mandy_has_pk = mandy.is_primary_key()
		mandy_pk = mandy.get_primary_key()
		mandy._set_default_primary_key()
		mandy_new_pk = mandy.get_primary_key()

		assert greg_pk == "pk"
		assert mandy_has_pk == False
		assert mandy_pk == None
		assert mandy_new_pk == 'id'


	def test_valid_field(self):
		assert greg.valid_field("age") == False
		assert greg.valid_field("name") == True
		assert mandy.valid_field("id") == True

	def test_insert(self):
		fields = list(greg._data.keys())
		values = list(greg._data.values())
		insert_sql = greg._get_insert_sql(fields)

		assert fields == ['pk', 'name']
		assert values == [1, 'Greg']
		assert insert_sql == "INSERT INTO user (pk, name) VALUES (%s, %s) RETURNING (pk)"

	def test_update(self):
		pk = greg._data[greg.get_primary_key()]
		values = ["Greg", pk]
		sql = greg._get_update_sql("name")

		assert pk == 1
		assert sql == "UPDATE user SET name=%s WHERE pk=%s"

	def test_subscribers(self):

		subscribers = greg.subscribers
		assert subscribers == []

	def test_query(self):
		assert isinstance(User.query(), Query) == True




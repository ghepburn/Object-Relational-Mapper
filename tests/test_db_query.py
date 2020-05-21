import pytest

from tests import db, Table, Column, ForeignKey


class Dog(Table):
	name = Column(str)
	age = Column(int)

db.create(Dog)

koda = Dog(name="Koda", age=2)
db.add(koda)

fin = Dog(name="Fin", age=2)
db.add(fin)

alex = Dog(name="Alex", age=10)
db.add(alex)

kevin = Dog(name="Kevin", age=5)
db.add(kevin)


class Test_Queries:

	def test_query_all(self):

		result = db.query(Dog).all()
		dogs = result.data

		assert len(dogs) == 4

		for pup in dogs:
			assert type(pup.id) == int
			assert isinstance(pup, Dog)

	def test_query_get(self):

		sql, fields, values =  Dog._get_select_where_sql(name="Koda")
		assert sql == "SELECT id, age, name FROM dog WHERE (name = %s)"
		assert fields == ['id', 'age', 'name']
		assert values == ['Koda']

		result = db.query(Dog).get(name="Koda")
		x = result.first()
		assert isinstance(x, Dog)
		assert x.name == "Koda"

		result = db.query(Dog).get(id='1')
		y = result.first()
		assert isinstance(y, Dog)
		assert y.id == 1
		assert y.name == "Koda"

		result = db.query(Dog).get(id='2', name='Fin')
		z = result.first()
		assert isinstance(z, Dog)
		assert z.id == 2
		assert z.name == "Fin"

	def test_query_orderby(self):

		result = db.query(Dog, order_by='id').all()
		dogs = result.data

		assert len(dogs) == 4
		assert dogs[0].id < dogs[1].id

		result = db.query(Dog, order_by="name").get()
		dogs = result.data

		assert len(dogs) == 4
		assert dogs[0].name < dogs[1].name

	def test_query_limit(self):

		# carl = Dog(name='carl')
		# dave = Dog(name='dave')
		# db.add(carl)
		# db.add(dave)

		result = db.query(Dog, limit=2).all()
		dogs = result.data
		assert len(dogs) == 2
		assert isinstance(dogs[0], Dog)

		dogs = db.query(Dog, limit='3').get().data
		assert len(dogs) == 3
		assert isinstance(dogs[0], Dog)

		dogs = db.query(Dog, order_by='name', limit=2).all().data
		assert len(dogs) == 2

	def test_complex_filter(self):

		results = db.query(Dog, order_by='age', limit=3).filter('age > 2')
		old_dogs = results.data

		results = db.query(Dog, order_by='age', limit=3).filter('name < K')
		alphabetical_dogs = results.data

		results = db.query(Dog, order_by='age', limit=3).filter('name<K')
		no_space_dogs = results.data

		for dog in old_dogs:
			assert dog.age > 2

		for dog in alphabetical_dogs:
			assert dog.name in ["Alex", "Fin"]

		for dog in no_space_dogs:
			assert dog.name in ["Alex", "Fin"]
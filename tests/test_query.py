from tests import orm, db

import pytest

Table = orm.Table
Column = orm.Column

class Planet(db.model):
	name = Column(str)
	age = Column(int)

db.create(Planet)

earth = Planet(name="Earth", age=550)
mars = Planet(name="Mars", age=770)
jupiter = Planet(name="Jupiter", age=300)

class Test_Query:

	def test_all(self):

		planets = Planet.query().all().data

		assert len(planets) == 3
		for aplanet in planets:
			assert isinstance(aplanet, Planet)

	def test_get(self):
		best_planet = Planet.query().get(name='Earth').first()
		youngest_planet = Planet.query().get(age=300).first()

		assert best_planet.name == "Earth" and best_planet.age == 550
		assert youngest_planet.name == "Jupiter" and youngest_planet.age == 300 

	def test_filter(self):
		old_planets = Planet.query().filter("age>400").data
		named_planets = Planet.query().filter('name<Earth').data

		assert len(old_planets) == 2
		for aplanet in old_planets:
			assert isinstance(aplanet, Planet)

		assert len(named_planets) == 0

	def test_orderby(self):
		ordered_planets = Planet.query().all(order_by="age").data
		reversed_planets = Planet.query().all(order_by="-age").data
		alpha_planets = Planet.query().all(order_by="name").data
		reversed_alpha_planets = Planet.query().all(order_by="-name").data


		assert ordered_planets[0].name == "Jupiter" and ordered_planets[-1].name == "Mars"
		assert reversed_planets[0].name == "Mars" and reversed_planets[-1].name == "Jupiter"
		assert alpha_planets[0].name == "Earth" and alpha_planets[-1].name == "Mars"
		assert reversed_alpha_planets[0].name == "Mars" and reversed_alpha_planets[-1].name == "Earth"

	def test_limit(self):
		limited_planets = Planet.query().all(limit=2).data

		assert len(limited_planets) == 2

	def test_mixed_args(self):

		double_arg = Planet.query().all(limit=2, order_by="-age").data
		irrelevant_args = Planet.query().get(name="Earth", limit=2, order_by="-age").data
		irrelevant_args2 = Planet.query().get(limit=2, order_by="-age", name="Earth").data
		filter_args = Planet.query().filter("id>1", limit=2, order_by="-id").data
		filter_args2 = Planet.query().filter("id>1", limit=1, order_by="id").data

		assert len(double_arg) == 2 and double_arg[0].name == "Mars"
		assert len(irrelevant_args) == 1 and irrelevant_args[0].name == 'Earth'
		assert len(irrelevant_args) == 1 and irrelevant_args[0].name == 'Earth'
		assert len(filter_args) == 2 and filter_args[0].id == 3
		assert len(filter_args2) == 1 and filter_args2[0].id == 2
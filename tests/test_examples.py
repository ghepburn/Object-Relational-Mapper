import pytest
from tests import db, orm

Table = orm.Table
Column = orm.Column
ForeignKey = orm.ForeignKey


class Department(Table):
	name = Column(str)
	summary = Column(str)
	num_of_employees = Column(int)

class Employee(Table):
	emp_num = Column(int, "primary_key")
	name = Column(str)
	department = ForeignKey(Department)

db.create(Department)
db.create(Employee)


class Test_Examples:

	def test_create(self):

		global hr, it, accounting, greg, rob, corey, matt

		hr = Department(name="Human Resources", summary="payroll and such", num_of_employees=2)
		it = Department(name="Information Technology", summary="computers and such", num_of_employees=1)
		accounting = Department(name="Accounting", summary="numbers and such", num_of_employees=5)

		cur = db.conn.cursor()
		cur.execute("SELECT * FROM employee")
		print(cur.fetchall())

		greg = Employee(emp_num=100, name="Greg", department=hr)
		rob = Employee(emp_num=101, name="Rob", department=accounting)
		corey = Employee(emp_num=102, name="Corey", department=it)
		matt = Employee(emp_num=103, name="Matt", department=accounting)

	# def test_read(self):
	# 	cur = db.conn.cursor()
	# 	cur.execute("SELECT * FROM employee")
	# 	print(cur.fetchall())

	# 	# x = Employee.query().all(limit=2, order_by="name").data
	# 	# y = Employee.query().get(name="Greg").first()		
	# 	# z = Employee.query().filter("emp_num>101", order_by="department").data

	# 	assert len(x) == 2 and x[0].name == "Corey" and x[1].name == "Greg"
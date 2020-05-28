import pytest
from tests import db, orm

Table = orm.Table
Column = orm.Column
ForeignKey = orm.ForeignKey

if "employee" in db.tables:
	db.drop_table("employee")
if "department" in db.tables:
	db.drop_table("department")


class Department(db.model):
	name = Column(str)
	summary = Column(str)
	num_of_employees = Column(int)

class Employee(db.model):
	emp_num = Column(int, "primary_key")
	name = Column(str)
	department = ForeignKey(Department)


class Test_Examples:

	def test_create(self):

		global hr, it, accounting, greg, rob, corey, matt

		db.create(Department)
		db.create(Employee)

		hr = Department(name="Human Resources", summary="payroll and such", num_of_employees=2)
		it = Department(name="Information Technology", summary="computers and such", num_of_employees=1)
		accounting = Department(name="Accounting", summary="numbers and such", num_of_employees=5)

		greg = Employee(emp_num=100, name="Greg", department=hr)
		rob = Employee(emp_num=101, name="Rob", department=accounting)
		corey = Employee(emp_num=102, name="Corey", department=it)
		matt = Employee(emp_num=103, name="Matt", department=accounting)


	def test_read(self):

		employees = Employee.query().all(order_by="name").data
		accountants = Employee.query().get(department=accounting).data	
		largest_department = Department.query().all(order_by="-num_of_employees", limit=1).first()
		specific = Employee.query().filter(["emp_num>101", "department=3"]).first()

		assert len(employees) == 4 and employees[0].name == "Corey" and employees[1].name == "Greg"
		assert len(accountants) == 2
		assert largest_department.name == "Accounting"
		assert specific.name == "Matt"

	def test_update(self):

		corey = Employee.query().get(name="Corey").first()
		corey.department = hr
		hr.num_of_employees = 3

		hr_employees = Employee.query().get(department=hr, order_by="name").data
		hr_num_employees = Department.query().get(name="Human Resources").first()

		assert len(hr_employees) == 2 and hr_employees[0].name == "Corey"
		assert hr_num_employees.num_of_employees == 3

	def test_delete(self):

		db.commit()

		employees = Employee.query().all().data
		matt = Employee.query().get(name="Matt").first()
		Employee.remove(matt)
		employees_after = Employee.query().all().data

		db.drop_table(Employee)

		assert len(employees) == 4
		assert matt.name == "Matt"
		assert len(employees_after) == 3
		assert "employee" not in db.tables

	def test_close(self):

		db.drop_table(Department)

		db.close()
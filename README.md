# Object-Relational-Mapper
Custom object relational mapper built in Python using only Psycopg2 third party library.

# How It Works
        from ORM import Database, Column, ForeignKey

1. instantiate a database object

        db = Database(host=XXX, database=XXX, user=XXX, password=XXX)

2. create python objects via database models

        class Department(db.model):
            name = Column(str)
    
        class Employee(db.model):
            emp_num = Column(str, "primary_key")
            name = Column(str)
            age = Column(int)
            department = ForeignKey(Department)
    
    
3. Perform database CRUD operations

- create
        db.create(department)
        db.create(Employee)
        IT = Department(name="information technology")
        greg = User(name="Greg", age=25, department=IT)

- read
        departments = Department.query().all()
        oldest_employee = Employee.query().get(order_by="age", limit=1)
        greg = Employee.query().get(name"Greg")

- update
        greg.age = 35
        IT.name="human resources"

- delete
        Department.remove(IT)
        db.drop_table(Employee)

- or manual SQL
        data = db.sql("SELECT * FROM EMPLOYEE")

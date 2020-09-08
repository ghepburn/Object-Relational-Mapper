# Object-Relational-Mapper
Custom object relational mapper built in Python using only Psycopg2 Postgres database third party library. This project was inspired by a curiosity of how SQLAlchemy worked, a desire to increase my knowledge how to work programmatically with databases 

# Description
This project was create using the popular Test Driven Development methodology.  Using PyTest Python library objectives were placed into tests. These tests failed, and then the logic of the ORM was built resolving these tests.

# How It Works
-	 from ORM import Database, Column, ForeignKey
-	
-	1. instantiate a database object
-	
-	        db = Database(host=XXX, database=XXX, user=XXX, password=XXX)
-	
-	2. create python objects via database models
-	
-	        class Department(db.model):
-	            name = Column(str)
-	    
-	        class Employee(db.model):
-	            emp_num = Column(str, "primary_key")
-	            name = Column(str)
-	            age = Column(int)
-	            department = ForeignKey(Department)
-	    
-	    
-	3. Perform database CRUD operations
-	
-	        create
-	        db.create(department)
-	        db.create(Employee)
-	        IT = Department(name="information technology")
-	        greg = User(name="Greg", age=25, department=IT)
-	
-	        read
-	        departments = Department.query().all()
-	        oldest_employee = Employee.query().get(order_by="age", limit=1)
-	        greg = Employee.query().get(name"Greg")
-	
-	        update
-	        greg.age = 35
-	        IT.name="human resources"
-	
-	        delete
-	        Department.remove(IT)
-	        db.drop_table(Employee)
-	
-	        or manual SQL
-	        data = db.sql("SELECT * FROM EMPLOYEE


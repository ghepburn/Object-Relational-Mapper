# Object-Relational-Mapper
Custom object relational mapper built in Python using only Psycopg2 third party library.

# How It Works
from ORM import Database

instantiate a database object
db = Database(host=XXX, database=XXX, user=XXX, password=XXX)

create python object via database models
fro ORM import Column, ForeignKey
class User(db.model):
    name = Column(str)
    age = Column(int)
    department = ForeignKey(department)
    
    
Perform database CRUD operations


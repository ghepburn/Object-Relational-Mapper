import os
import sys
sys.path.append("C:\\Users\\Greg\\Python_Projects\\WebDevelopment\\orm")

password = os.environ.get("GREGDB_PASSWORD")

import orm
Database = orm.Database
Table = orm.Table
Column = orm.Column
ForeignKey = orm.ForeignKey
Query = orm.Query

db = orm.Database(host='localhost', database='gregdb', user='postgres', password=password)
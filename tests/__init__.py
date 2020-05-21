import os
import sys
sys.path.append("C:\\Users\\Greg\\Python_Projects\\WebDevelopment\\orm")

password = os.environ.get("GREGDB_PASSWORD")

from orm import Database, Table, Column, ForeignKey

db = Database(host='localhost', database='gregdb', user='postgres', password=password)
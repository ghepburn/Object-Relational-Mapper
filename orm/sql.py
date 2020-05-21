
GET_ALL_TABLES_SQL = "SELECT table_name FROM information_schema.tables"

TABLE_SELECT_SQL = "SELECT {fields} FROM {name}"
TABLE_CREATE_SQL = "CREATE TABLE {name} ({fields})"
TABLE_INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders}) RETURNING (id)"
TABLE_UPDATE_SQL = "UPDATE {name} SET {field}=%s WHERE {filter}=%s"
TABLE_SELECT_WHERE_SQL = "SELECT {fields} FROM {name} WHERE ({filters})"
TABLE_DROP_SQL = "DROP TABLE {name}"

COLUMN_CREATE_SQL = "{name} {type}"
FOREIGNKEY_CREATE_SQL = "{name} {type} REFERENCES {table} {table_name}"

INSTANCE_DELETE_SQL ="DELETE FROM {table} WHERE {field}={placeholder}"

ORDERBY_SQL = " ORDER BY {field}"
LIMIT_SQL = " LIMIT {number}"

class SQL_Factory:
	def get_sql(self, argument, value):
		if argument == 'limit':
			sql = LIMIT_SQL
			sql = sql.format(number=value)
		elif argument == 'order_by':
			sql = ORDERBY_SQL
			sql = sql.format(field=value)	
		return sql
		
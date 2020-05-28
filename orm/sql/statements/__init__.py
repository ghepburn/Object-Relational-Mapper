

GET_ALL_TABLES_SQL = "SELECT table_name FROM information_schema.tables WHERE (table_schema='public') ORDER BY table_name"

TABLE_SELECT_SQL = "SELECT {fields} FROM {table}"
TABLE_CREATE_SQL = "CREATE TABLE {table} ({fields})"
TABLE_INSERT_SQL = "INSERT INTO {table} ({fields}) VALUES ({placeholders}) RETURNING ({pk})"
TABLE_UPDATE_SQL = "UPDATE {table} SET {field}=%s WHERE {pk}=%s"
TABLE_SELECT_WHERE_SQL = "SELECT {fields} FROM {table} WHERE {filters}"
TABLE_DROP_SQL = "DROP TABLE {table}"

COLUMN_CREATE_SQL = "{name} {type}"
COLUMN_PK_CREATE_SQL = COLUMN_CREATE_SQL + " PRIMARY KEY"
FOREIGNKEY_CREATE_SQL = "{name} {type} REFERENCES {table}({field})"

INSTANCE_DELETE_SQL ="DELETE FROM {table} WHERE {filters}"

ORDERBY_ASC_SQL = " ORDER BY {field} ASC"
ORDERBY_DESC_SQL = " ORDER BY {field} DESC"
LIMIT_SQL = " LIMIT {number}"
FIELDS_SQL = "{fields}"
FIELD_FILTER_SQL = "{field}{operator}{placeholder}"

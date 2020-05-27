GET_ALL_TABLES_SQL = "SELECT table_name FROM information_schema.tables"

TABLE_SELECT_SQL = "SELECT {fields} FROM {table}"
TABLE_CREATE_SQL = "CREATE TABLE {table} ({fields})"
TABLE_INSERT_SQL = "INSERT INTO {table} ({fields}) VALUES ({placeholders}) RETURNING (id)"
TABLE_UPDATE_SQL = "UPDATE {table} SET {field}=%s WHERE {pk}=%s"
TABLE_SELECT_WHERE_SQL = "SELECT {fields} FROM {table} WHERE ({filters})"
TABLE_DROP_SQL = "DROP TABLE {table}"
import mysql.connector
from mysql.connector.cursor import CursorBase


class MySQLTool:
  def __init__(self, host, user, password, database):
    try:
      self.mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        collation='utf8mb4_general_ci',
      )
    except mysql.connector.Error as err:
      print(f"Error connecting to MySQL: {err}")
      self.mydb = None

  def execute(self, sql_query: str):
    """
    # Execute an SQL query and return the results as a string.
    sql_query: The SQL query to execute.
    """
    if self.mydb is None or not self.mydb.is_connected():
      return {'ok': False, 'error': 'Not connected to MySQL.'}

    try:
      cursor: CursorBase = self.mydb.cursor(buffered=True)
      cursor.execute(sql_query)

      if len(cursor.description) > 0:
        results = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        formatted_results = "\n".join([f"{'|'.join(map(str, row))}" for row in results])
        header = " | ".join(column_names)
        separator = "-|-".join(['-' * len(col) for col in column_names])
        formatted_results = f"{header}\n{separator}\n{formatted_results}"
      else:
        formatted_results = "(no rows returned)"

      data = {
        'query': sql_query,
        'results': formatted_results,
        'count': cursor.rowcount,
      }
      return data

    except mysql.connector.Error as err:
      return {'ok': False, 'error': f"Error executing SQL: {err}"}
    finally:
      if 'mycursor' in locals():
        cursor.close()
        # Do not close the connection here, as the tool instance might be used for multiple queries
        # The user should handle closing the connection when the tool is no longer needed.

  def close_connection(self):
    if self.mydb and self.mydb.is_connected():
      self.mydb.close()

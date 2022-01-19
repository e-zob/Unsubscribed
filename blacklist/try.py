from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user='ellie',
        password='Password',
        database='hubXchange_unsubscribed'
    ) as connection:
        show_table_query="SELECT * FROM unsubscribed"
        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            # Fetch rows from last executed query
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
    print(e)
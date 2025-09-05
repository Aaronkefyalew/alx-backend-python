
import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that streams rows from user_data one by one."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # <-- change this
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)  # fetch rows as dicts
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error while streaming users: {e}")

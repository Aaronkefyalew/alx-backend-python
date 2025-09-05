
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """Generator that fetches users in batches from user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # <-- change this
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows  # yield each batch at once

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming in batches: {e}")


def batch_processing(batch_size):
    """
    Processes each batch of users:
    - Only yields users with age > 25
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if int(user["age"]) > 25:
                yield user

#!/usr/bin/python3
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
                cursor.close()
                connection.close()
                return  # ✅ use return to stop generator
            yield rows

    except Error as e:
        print(f"Error streaming in batches: {e}")
        return


def batch_processing(batch_size):
    """Generator that yields users over age 25 from batches."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user["age"]) > 25:
                yield user
    return  # ✅ stops when all batches are processed



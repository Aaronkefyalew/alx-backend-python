#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # <-- change this
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:  # ✅ loop 1
            yield int(row["age"])

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming ages: {e}")


def calculate_average_age():
    """Calculate and print average age without loading all data into memory."""
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ loop 2
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")

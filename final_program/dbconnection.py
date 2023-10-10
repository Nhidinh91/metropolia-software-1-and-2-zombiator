import mysql.connector


def db_connection():
    try:
        connection = mysql.connector.connect(
            user="root",
            password="123456",
            host="localhost",
            port=3306,
            database="zombiator",
            autocommit=True,
        )
        cursor = connection.cursor()

        return connection, cursor  # Return both the connection and cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

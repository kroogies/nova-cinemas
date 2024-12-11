import mysql.connector
from mysql.connector import Error

try:
    # Establish a connection to the database
    connection = mysql.connector.connect(
        host='localhost',      # e.g., 'localhost'
        database='novacinemas',    # e.g., 'your_database'
        user='root',      # e.g., 'root'
        password='minimumM4.'  # e.g., 'your_password'
    )

    if connection.is_connected():
        print("Connected to the database")

        # Create a cursor object using the connection
        cursor = connection.cursor()

        # Define the CREATE TABLE query
        create_table_query = '''
        DROP TABLE reservations
        '''

        # Execute the query
        cursor.execute(create_table_query)

        # Commit the changes
        connection.commit()
        print("Table 'bookings' created successfully")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

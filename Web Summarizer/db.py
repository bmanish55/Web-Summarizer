import mysql.connector

# Replace with your MySQL credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Manish@845905',
    'database': 'websummerizer'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("Connection successful")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")

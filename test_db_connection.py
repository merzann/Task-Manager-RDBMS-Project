import psycopg2
try:
    connection = psycopg2.connect(
        dbname="taskmanager", 
        user="gitpod", 
        password="your_password", 
        host="localhost", 
        port="5432"
    )
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()

# db.py
import mysql.connector

def get_db_connection():
    db_config = {
        'host': '36.94.112.125',
        'user': 'it_dev',
        'password': 'MyPassword1!',  # Ubah jika ada password
        'database': 'dashboard',
        'port': '3306',
       
        
    }

    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

import mysql.connector
import csv

class MB51GRModel:
    def __init__(self):
        self.db_config = {
            'host': '36.94.112.125',
            'user': 'it_dev',
            'password': 'MyPassword1!',  # Ubah jika ada password
            'database': 'dashboard',
            'port': '3306',
       
        }

    def save_to_database(self, csv_file, selected_columns):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Truncate the table to remove existing data
            truncate_query = f"TRUNCATE TABLE mb51_gr"
            cursor.execute(truncate_query)

            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Get the header row

                sql_header = ', '.join([f"`{col}`" for col in selected_columns])
                insert_query = f"INSERT INTO mb51_gr ({sql_header}) VALUES ({', '.join(['%s'] * len(selected_columns))})"

                for row in reader:
                    filtered_row = [row[header.index(col)] for col in selected_columns]
                    cursor.execute(insert_query, filtered_row)

            conn.commit()
            print("Data successfully inserted into the database.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

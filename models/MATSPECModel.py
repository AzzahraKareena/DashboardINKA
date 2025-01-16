import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_matspec_data(file_path):
    csv_path = convert_html_to_csv(file_path)
    insert_into_database(csv_path)

def convert_html_to_csv(file_path):
    soup = BeautifulSoup(open(file_path, 'r', encoding='utf-8'), 'html.parser')
    csv_file = file_path.replace('.htm', '.csv')
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                data = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                writer.writerow(data)
                
    return csv_file

def insert_into_database(csv_path):
    conn = mysql.connector.connect(
       host="36.94.112.125",  # IP server database
        user="it_dev",             # Username database
        password="MyPassword1!",   # Password database
        database="dashboard", 
        port = 3306 
    )
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE matspec")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sql = """
            INSERT INTO matspec 
            (`Material`, `Material_Description`, `Text`, `Base_Unit_of_Measure`, `Material_Group`, `Material_Type`, 
            `Plant`, `DF_at_client_level`, `Valuation_Class`, `Created_by`, `Last_Change`, `Price`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                row['Material'], 
                row['Material Description'], 
                row['Text (200 chars.)'], 
                row['Base Unit of Measure'], 
                row['Material Group'], 
                row['Material Type'], 
                row['Plant'], 
                row['DF at client level'], 
                row['Valuation Class'], 
                row['Created by'], 
                row['Last Change'], 
                row['Price']
            ))

    conn.commit()
    cursor.close()
    conn.close()

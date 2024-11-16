import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_cn55n_data(file_path):
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
        host="36.94.112.123",  # IP server database
        user="it",             # Username database
        password="ITIMS321",   # Password database
        database="dashboard",  # Nama database
        port=3306              # Port MySQL (default: 3306)
    )
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE CN55N")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sql = "INSERT INTO CN55N (`Project_Definition`, `WBS_Element`, `Sales_Document`, `Sales_Document_Item`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (row['Project Definition'], row['WBS Element'],row['Sales Document'],row['Sales Document Item']))

    conn.commit()
    cursor.close()
    conn.close()

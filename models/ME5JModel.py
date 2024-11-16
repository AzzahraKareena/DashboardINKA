import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_me5j_data(file_path):
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
    cursor.execute("TRUNCATE TABLE ME5J")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
           sql = "INSERT INTO me5j (`WBS_Element`, `Purchase_Requisition`, `Item_of_Requisition`, `Requisition_Date`, `Deliv.date(From/to)`, `Deletion_Indicator`, `Processing_status`, `Material`, `Short_Text`, `Material_Group`, `Requisitioner`, `Purchasing_Group`, `Quantity_Requested`, `Unit_of_Measure`, `Purchase_Order`, `Purchase_Order_Date`, `Purchase_Order_Item`, `Quantity_Ordered`, `Document_Type`, `Storage_Location`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
           cursor.execute(sql, (row['WBS Element'], row['Purchase Requisition'], row['Item of Requisition'], row['Requisition Date'], row['Deliv. date(From/to)'], row['Deletion Indicator'], row['Processing status'], row['Material'], row['Short Text'], row['Material Group'], row['Requisitioner'], row['Purchasing Group'], row['Quantity Requested'], row['Unit of Measure'], row['Purchase Order'], row['Purchase Order Date'], row['Purchase Order Item'], row['Quantity Ordered'], row['Document Type'], row['Storage Location']))

    conn.commit()
    cursor.close()
    conn.close()

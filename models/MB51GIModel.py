import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_mb51_gi_data(file_path):
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
    cursor.execute("TRUNCATE TABLE MB51_GI")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            sql = """
            INSERT INTO mb51_gi 
            (`Posting_Date`, `Material`, `Material_Description`, `Purchase_Order`, `Document_Date`, 
            `Qty_in_Un.of_Entry`, `Item`, `Movement_Type`, `WBS_Element`, `Unit_of_Entry`, `Amount_in_LC`, 
            `Material_Document`, `User_Name`, `Document_Header_Text`, `Reference`, `Order`, `Vendor`, `Reservation`, `Batch`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            """
            
            # Debug: Print number of placeholders and values being passed
            values = (
                row['Posting Date'], row['Material'], row['Material Description'], row['Purchase Order'], row['Document Date'],
                row['Qty in Un. of Entry'], row['Item'], row['Movement Type'], row['WBS Element'], row['Unit of Entry'], 
                row['Amount in LC'], row['Material Document'], row['User Name'], row['Document Header Text'], 
                row['Reference'], row['Order'], row['Vendor'], row['Reservation'], row['Batch']
            )
            print(f"Values: {values}")  # Check the values being passed
            cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()



import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_va05_data(file_path):
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
    cursor.execute("TRUNCATE TABLE VA05")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sql = "INSERT INTO VA05 (`Sales_Document`, `Sales_Document_Type`, `Document_Date`, `Purchase_order_number`, `Status`, `Item_(SD)`, `Description`, `Material`, `Confirmed_Quantity`, `Delivery_Date`, `Created_by`, `Sold-to_party`, `Name_1`, `Exchange_Rate`, `Order_Quantity`, `Base_Unit_of_Measure`, `Net_price`, `Pricing_unit`, `Unit_of_measure`, `Pricing_date`, `Net_Value`, `Document_Currency`, `Goods_Issue_Date`, `Created_on`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row['Sales Document'], row['Sales Document Type'], row['Document Date'], row['Purchase order number'], row['Status'], row['Item (SD)'], row['Description'], row['Material'], row['Confirmed Quantity'], row['Delivery Date'], row['Created by'], row['Sold-to party'], row['Name 1'], row['Exchange Rate'], row['Order Quantity'], row['Base Unit of Measure'], row['Net price'], row['Pricing unit'], row['Unit of measure'], row['Pricing date'], row['Net Value'], row['Document Currency'], row['Goods Issue Date'], row['Created on']))



    conn.commit()
    cursor.close()
    conn.close()

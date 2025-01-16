import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_me2j_data(file_path):
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
    cursor.execute("TRUNCATE TABLE me2j")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sql = "INSERT INTO me2j (`WBS_Element`, `Purchase_Order`, `Item`, `Material`, `Deletion_Indicator`, `Short_Text`, `Order_Quantity`, `Order_Unit`, `Document_Date`, `Vendor/supplying_plant`, `Still_to_be_delivered_(value)`, `Still_to_be_invoiced_(qty)`, `Still_to_be_invoiced_(val.)`, `Net_price`, `Still_to_be_delivered_(qty)`, `Currency`, `Acct_Assignment_Cat.`, `PO_history/release_documentation`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row['WBS Element'], row['Purchasing Document'], row['Item'], row['Material'], row['Deletion Indicator'], row['Short Text'], row['Order Quantity'], row['Order Unit'], row['Document Date'], row['Vendor/supplying plant'], row['Still to be delivered (value)'], row['Still to be invoiced (qty)'], row['Still to be invoiced (val.)'], row['Net price'], row['Still to be delivered (qty)'], row['Currency'], row['Acct Assignment Cat.'], row['PO history/release documentation']))

    conn.commit()
    cursor.close()
    conn.close()

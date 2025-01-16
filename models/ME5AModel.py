import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_me5a_data(file_path):
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
    cursor.execute("TRUNCATE TABLE me5a")  # Hapus data lama

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
                sql = """
                    INSERT INTO me5a (
                        acct_assignment_cat, requisitioner, purchase_requisition, 
                        req_tracking_number, item_of_requisition, release_indicator, 
                        requisition_date, release_date, changed_on, deliv_date, deletion_indicator, processing_status, 
                        material, short_text, unit_of_measure, material_group, 
                        purchasing_group, closed
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    row['Acct Assignment Cat.'], 
                    row['Requisitioner'], 
                    row['Purchase Requisition'], 
                    row['Req. Tracking Number'], 
                    row['Item of Requisition'], 
                    row['Release indicator'], 
                    row['Requisition Date'], 
                    row['Release Date'], 
                    row['Changed on'], 
                    row['Deliv. date(From/to)'],  
                    row['Deletion Indicator'], 
                    row['Processing status'], 
                    row['Material'], 
                    row['Short Text'], 
                    row['Unit of Measure'], 
                    row['Material Group'], 
                    row['Purchasing Group'], 
                    row['Closed']
                ))

    conn.commit()
    cursor.close()
    conn.close()

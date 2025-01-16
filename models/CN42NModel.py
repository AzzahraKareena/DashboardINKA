import csv
import mysql.connector
from bs4 import BeautifulSoup

def process_cn42n_data(file_path):
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
    # Konfigurasi koneksi ke database
    conn = mysql.connector.connect(
        host="36.94.112.125",  # IP server database
        user="it_dev",             # Username database
        password="MyPassword1!",   # Password database
        database="dashboard", 
        port = 3306 
    )

    # Membuat cursor
    cursor = conn.cursor()

    try:
        # Hapus data lama dari tabel CN42N
        cursor.execute("TRUNCATE TABLE cn42n")
        print("Data lama dihapus.")

        # Buka file CSV dan baca isinya
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Insert setiap baris data ke database
            for row in reader:
                sql = "INSERT INTO cn42n (`Project_definition`, `Name`) VALUES (%s, %s)"
                cursor.execute(sql, (row['Project definition'], row['Name']))
        
        # Commit transaksi
        conn.commit()
        print("Data berhasil dimasukkan ke database.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup cursor dan koneksi
        cursor.close()
        conn.close()

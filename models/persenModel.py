import csv
import mysql.connector
from datetime import datetime

def process_persen_data(file_path):
    # Memastikan file yang diproses adalah CSV
    if not file_path.endswith('.csv'):
        print(f"File {file_path} bukan file CSV. Proses dibatalkan.")
        return

    insert_into_database(file_path)

def insert_into_database(csv_path):
    try:
        conn = mysql.connector.connect(
            host="36.94.112.125",  # IP server database
        user="it_dev",             # Username database
        password="MyPassword1!",   # Password database
        database="dashboard", 
        port = 3306 
        
        )

        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE persen")  # Hapus data lama

            # Baca file CSV dan masukkan data ke tabel 'persen'
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Menyiapkan query SQL
                    sql = """
                        INSERT INTO persen (
                            project_def, WBS_element, Sales_Document, so_date, customer_po_number, 
                            sold_to_party, material_code, material_name, no, qty_so, uom, 
                            unit_price_so, total_price_so, deliver_qty, uom_1, unit_price_do, 
                            delivered, to_be_deliver_qty, invoiced_qty, uom_2, unit_price_invoice, 
                            total_price_billing, to_be_invoiced, po_date, req_dlv_dt, duration_in_days, 
                            status, persen
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        row['PROJECT DEF'], 
                        row['WBS_element'], 
                        row['Sales_Document'], 
                        row['SO DATE'],  # Biarkan tanggal dalam format aslinya
                        row['CUSTOMER PO NUMBER'], 
                        row['Sold-to_party'], 
                        row['MATERIAL CODE'], 
                        row['MATERIAL NAME'], 
                        row['NO'], 
                        row['QTY SO'], 
                        row['UOM.1'], 
                        row['UNIT PRICE SO'], 
                        row['TOTAL PRICE SO'], 
                        row['DELIVER QTY'], 
                        row['UOM.1'], 
                        row['UNIT PRICE DO'], 
                        row['DELIVERED'], 
                        row['TO BE DELIVER QTY'], 
                        row['INVOICED QTY'], 
                        row['UOM.2'], 
                        row['UNIT PRICE INVOICE'], 
                        row['TOTAL PRICE BILLING'], 
                        row['TO BE INVOICED'], 
                        row['PO date'],  # Biarkan tanggal dalam format aslinya
                        row['Req.dlv.dt'],  # Biarkan tanggal dalam format aslinya
                        row['Duration (in days)'], 
                        row['Status'], 
                        row['Persen']
                    ))

            conn.commit()
            print(f"Data dari {csv_path} berhasil dimasukkan ke dalam database.")
    except Exception as e:
        print(f"Terjadi kesalahan saat memasukkan data ke database: {e}")
    finally:
        conn.close()

import csv
import mysql.connector
from datetime import datetime

def process_barang_data(file_path):
    # Memastikan file yang diproses adalah CSV
    if not file_path.endswith('.csv'):
        print(f"File {file_path} bukan file CSV. Proses dibatalkan.")
        return

    insert_into_database(file_path)

def insert_into_database(csv_path):
    try:
        conn = mysql.connector.connect(
            host="localhost",  # IP server database
            user="root",             # Username database
            password="",   # Password database
            database="dashboard",  # Nama database
            # Ganti dengan nama database Anda
        )

        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE barang")  # Hapus data lama

            # Baca file CSV dan masukkan data ke tabel 'persen'
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Menyiapkan query SQL
                    sql = """
                        INSERT INTO barang (
                            project_def, wbs_element, so_document, so_date, req_delivery_date, duration, customer_po_number, customer_code,
                            customer_name, material_code, material_name, no, qty_so, uom, unit_price_so, total_price_so, deliver_qty, 
                            uom_1, unit_price_do,total_price_do, to_be_deliver_qty, invoiced_qty, uom_2, unit_price_billing, 
                            total_price_billing, to_be_invoice, status,unit_price_invoice ,to_be_deliver_invoice 
                        ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        row['PROJECT DEF'], 
                        row['WBS ELEMENT'], 
                        row['SO DOCUMENT'], 
                        row['SO DATE'],  # Tanggal dibiarkan dalam format aslinya
                        row['REQ DELIVERY DATE'],  # Tanggal dibiarkan dalam format aslinya
                        row['DURATION'], 
                        row['CUSTOMER PO NUMBER'], 
                        row['CUSTOMER CODE'], 
                        row['CUSTOMER NAME'], 
                        row['MATERIAL CODE'], 
                        row['MATERIAL NAME'], 
                        row['NO'], 
                        row['QTY SO'], 
                        row['UOM'], 
                        row['UNIT PRICE SO'], 
                        row['TOTAL PRICE SO'], 
                        row['DELIVER QTY'], 
                        row['UOM_1'], 
                        row['UNIT PRICE DO'], 
                        row['TOTAL PRICE DO'], 
                        row['TO BE DELIVER QTY'], 
                        row['INVOICED QTY'], 
                        row['UOM_2'], 
                        row['UNIT PRICE BILLING'], 
                        row['TOTAL PRICE BILLING'], 
                        row['TO BE INVOICE'], 
                        row['STATUS'], 
                        row['UNIT PRICE INVOICE'], 
                        row['TO BE DELIVER INVOICE']
                    ))

            conn.commit()
            print(f"Data dari {csv_path} berhasil dimasukkan ke dalam database.")
    except Exception as e:
        print(f"Terjadi kesalahan saat memasukkan data ke database: {e}")
    finally:
        conn.close()

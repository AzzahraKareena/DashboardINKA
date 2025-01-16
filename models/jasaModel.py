import csv
import mysql.connector
from datetime import datetime

def process_jasa_data(file_path):
    # Memastikan file yang diproses adalah CSV
    if not file_path.endswith('.csv'):
        print(f"File {file_path} bukan file CSV. Proses dibatalkan.")
        return

    insert_into_database(file_path)

def insert_into_database(csv_path):
    try:
        # Koneksi ke database
        conn = mysql.connector.connect(
        host="36.94.112.125",  # IP server database
            user="it_dev",             # Username database
            password="MyPassword1!",   # Password database
            database="dashboard", 
            port = 3306  # Nama database
            
        )
        cursor = conn.cursor()

        # Truncate tabel untuk membersihkan data lama
        cursor.execute("TRUNCATE TABLE jasa")
        conn.commit()  # Pastikan truncate diterapkan

        # Baca file CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Debug: cek data yang dibaca
                print(f"Memproses row: {row}")

                # Ambil nilai kolom, gunakan nilai default jika kolom tidak ada
                values = (
                    row.get('PROJECT DEF', '').strip(),
                    row.get('WBS_element', '').strip(),
                    row.get('Sales_Document', '').strip(),
                    row.get('SO DATE', '').strip(),
                    row.get('CUSTOMER PO NUMBER', '').strip(),
                    row.get('Sold-to_party', '').strip(),
                    row.get('CUSTOMER NAME', '').strip(),
                    row.get('MATERIAL CODE', '').strip(),
                    row.get('MATERIAL NAME', '').strip(),
                    row.get('NO_ITEM', '').strip(),
                    row.get('QTY SO', '0').strip(),
                    row.get('UOM', '').strip(),
                    row.get('UNIT PRICE SO', '0').strip(),
                    row.get('TOTAL PRICE SO', '0').strip(),
                    row.get('TOTAL PRICE BILLING', '0').strip(),
                    row.get('SISA PRICE BILLING', '0').strip(),
                    row.get('STATUS', '0').strip()  # Periksa kolom ini
                )

                # Query SQL untuk insert data
                sql = """
                    INSERT INTO jasa (
                        project_def, wbs_element, sales_document, so_date, customer_po_number,
                        sold_to_party, customer_name, material_code, material_name, no_item, qty_so, uom,
                        unit_price_so, total_price_so, total_price_billing, sisa_price_billing, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
                """
                # Eksekusi query
                cursor.execute(sql, values)

        # Commit semua perubahan
        conn.commit()
        print(f"Data dari {csv_path} berhasil dimasukkan ke dalam database.")
    
    except mysql.connector.Error as err:
        print(f"Kesalahan MySQL: {err}")
        conn.rollback()  # Rollback jika terjadi error
    except Exception as e:
        print(f"Kesalahan: {e}")
    finally:
        # Tutup koneksi
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn:
            conn.close()

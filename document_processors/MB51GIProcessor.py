import os
import csv
from bs4 import BeautifulSoup

class MB51GIProcessor:
    header_mapping = {
        'Posting Date': 'Posting_Date',
        'Material': 'Material',
        'Material Description': 'Material_Description',
        'Purchase Order': 'Purchase_Order',
        'Document Date': 'Document_Date',
        'Qty in Un. of Entry': 'Qty_in_Un_of_Entry',
        'Item': 'Item',
        'Movement Type': 'Movement_Type',
        'WBS Element': 'WBS_Element',
        'Unit of Entry': 'Unit_of_Entry',
        'Amount in LC': 'Amount_in_LC',
        'Material Document': 'Material_Document',
        'User Name': 'User_Name',
        'Document Header Text': 'Document_Header_Text',
        'Reference': 'Reference',
        'Order': 'Order',
        'Vendor': 'Vendor',
        'Reservation': 'Reservation',
        'Batch': 'Batch'
    }


    @staticmethod
    def mhtml_to_csv(mhtml_file, output_csv):
        try:
            with open(mhtml_file, 'r', encoding='utf-8') as file:
                mhtml_content = file.read()

            soup = BeautifulSoup(mhtml_content, 'html.parser')
            tables = soup.find_all('table')

            # Menggunakan tabel pertama
            if tables:
                table = tables[0]
                header_row = table.find('tr')
                if header_row:
                    header = [col.get_text().strip() for col in header_row.find_all(['th', 'td'])]
                    mapped_header = MB51GIProcessor.map_headers(header)

                    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(mapped_header)

                        rows = table.find_all('tr')[1:]  # Lewati baris header
                        for row in rows:
                            cols = row.find_all('td')
                            writer.writerow([col.get_text().strip() for col in cols])

        except FileNotFoundError:
            print(f"File {mhtml_file} tidak ditemukan.")
        except Exception as e:
            print(f"Kesalahan saat mengonversi file MHTML: {e}")

    @staticmethod
    def map_headers(header):
        return [MB51GIProcessor.header_mapping.get(col, col) for col in header]

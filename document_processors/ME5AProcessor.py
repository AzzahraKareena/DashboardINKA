import os
import csv
from bs4 import BeautifulSoup

class ME5AProcessor:
    header_mapping = {
        'Acct Assignment Cat.': 'acct_assignment_cat',
        'Requisitioner': 'requisitioner',
        'Purchase Requisition': 'purchase_requisition',
        'Req. Tracking Number': 'req_tracking_number',
        'Item of Requisition': 'item_of_requisition',
        'Release indicator': 'release_indicator',
        'Requisition Date': 'requisition_date',
        'Release Date': 'release_date',
        'Changed on': 'changed_on',
        'Deliv. date(From/to)': 'deliv_date',
        'Deletion Indicator': 'deletion_indicator',
        'Processing status': 'processing_status',
        'Material': 'material',
        'Short Text': 'short_text',
        'Unit of Measure': 'unit_of_measure',
        'Material Group': 'material_group',
        'Purchasing Group': 'purchasing_group',
        'Closed': 'closed'
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
                    mapped_header = ME5AProcessor.map_headers(header)

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
        return [ME5AProcessor.header_mapping.get(col, col) for col in header]

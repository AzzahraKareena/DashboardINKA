import os
import csv
from bs4 import BeautifulSoup

class ME2JProcessor:
    header_mapping = {
        'WBS Element': 'WBS_Element',
        'Purchasing Document': 'Purchasing_Document',
        'Item': 'Item',
        'Material': 'Material',
        'Deletion Indicator': 'Deletion_Indicator',
        'Short Text': 'Short_Text',
        'Order Quantity': 'Order_Quantity',
        'Order Unit': 'Order_Unit',
        'Document Date': 'Document_Date',
        'Vendor/supplying plant': 'Vendor/supplying_plant',
        'Still to be delivered (value)': 'Still_to_be_delivered_(value)',
        'Still to be invoiced (qty)': 'Still_to_be_invoiced_(qty)',
        'Still to be invoiced (val.)': 'Still_to_be_invoiced_(val.)',
        'Net price': 'Net_price',
        'Still to be delivered (qty)': 'Still_to_be_delivered_(qty)',
        'Currency': 'Currency',
        'Acct Assignment Cat.': 'Acct_Assignment_Cat.',
        'PO history/release documentation': 'PO_history/release_documentation'
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
                    mapped_header = ME2JProcessor.map_headers(header)

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
        return [ME2JProcessor.header_mapping.get(col, col) for col in header]

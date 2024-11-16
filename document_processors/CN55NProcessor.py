import os
import csv
from bs4 import BeautifulSoup

class CN55NProcessor:
    header_mapping = {
        'Project Definition': 'Project_Definition',
        'WBS Element': 'WBS_Element',
        'Sales Document': 'Sales_Document',
        'Sales Document Item':'Sales_Document_Item'
        
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
                    mapped_header = CN55NProcessor.map_headers(header)

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
        return [CN55NProcessor.header_mapping.get(col, col) for col in header]

import os
import csv
from bs4 import BeautifulSoup

class MB52Processor:
    # Pemetaan kolom header yang sesuai dengan kolom di database atau format yang diinginkan
    header_mapping = {
        'Material': 'Material',
        'Plnt': 'Plnt',
        'SLoc': 'SLoc',
        'S': 'S',
        'Special stock number': 'WBS_Element',  # Memetakan 'Special stock number' ke 'WBS Element' dalam database
        'BUn': 'BUn',
        'Unrestricted': 'Unrestricted',
        'Crcy': 'Crcy',
        'Value Unrestricted': 'Value_Unrestricted'
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
                    # Mengambil header tabel dan memetakannya
                    header = [col.get_text().strip() for col in header_row.find_all(['th', 'td'])]
                    mapped_header = MB52Processor.map_headers(header)

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
        # Memetakan kolom yang ditemukan pada header HTML ke header yang sesuai
        return [MB52Processor.header_mapping.get(col, col) for col in header]


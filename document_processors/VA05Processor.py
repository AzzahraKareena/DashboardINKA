import os
import csv
from bs4 import BeautifulSoup

class VA05Processor:
    header_mapping = {
        'Sales Document': 'Sales_Document',
        'Sales Document Type': 'Sales_Document_Type',
        'Document Date': 'Document_Date',
        'Purchase order number': 'Purchase_order_number',
        'Status': 'Status',
        'Item (SD)': 'Item_(SD)',
        'Description': 'Description',
        'Material': 'Material',
        'Confirmed Quantity': 'Confirmed_Quantity',
        'Delivery Date': 'Delivery_Date',
        'Created by': 'Created_by',
        'Sold-to party': 'Sold-to_party',
        'Name 1': 'Name_1',
        'Exchange Rate': 'Exchange_Rate',
        'Order Quantity': 'Order_Quantity',
        'Base Unit of Measure': 'Base_Unit_of_Measure',
        'Net price': 'Net_price',
        'Pricing unit': 'Pricing_unit',
        'Unit of measure': 'Unit_of_measure',
        'Pricing date': 'Pricing_date',
        'Net Value': 'Net_Value',
        'Document Currency': 'Document_Currency',
        'Goods Issue Date': 'Goods_Issue_Date',
        'Created on': 'Created_on'
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
                    mapped_header = VA05Processor.map_headers(header)

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
        return [VA05Processor.header_mapping.get(col, col) for col in header]
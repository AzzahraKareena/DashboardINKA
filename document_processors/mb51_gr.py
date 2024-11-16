import os
import csv
from bs4 import BeautifulSoup

class MB51GRProcessor:
    header_mapping = {
        'MB51_GR': {
            'Posting Date': 'Posting_Date',
            'Material': 'Material',
            'Material Description': 'Material_Description',
            'Purchase Order': 'Purchase_Order',
            'Document Date': 'Document_Date',
            'Qty in Un. of Entry': 'Qty_in_Un_of_Entry',
            'Item PO': 'Item_PO',
            'Movement Type': 'Movement_Type',
            'WBS Element': 'WBS_Element',
            'Unit of Entry': 'Unit_of_Entry',
            'Item GR': 'Item_GR',
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
    }

    def mhtml_to_csv(self, mhtml_file, output_csv):
        try:
            with open(mhtml_file, 'r', encoding='utf-8') as file:
                mhtml_content = file.read()
        except FileNotFoundError:
            print(f"File {mhtml_file} not found.")
            return

        soup = BeautifulSoup(mhtml_content, 'html.parser')
        tables = soup.find_all('table')

        for table_index, table in enumerate(tables):
            if table_index == 0:
                csv_file = output_csv
            else:
                csv_file = output_csv.replace('.csv', f'_{table_index + 1}.csv')

            header_row = table.find('tr')
            if header_row:
                header = [col.get_text().strip() for col in header_row.find_all(['th', 'td'])]
                mapped_header = self.map_headers(header)

                with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(mapped_header)

                    rows = table.find_all('tr')[1:]  # Skip header row
                    for row in rows:
                        cols = row.find_all('td')
                        writer.writerow([col.get_text().strip() for col in cols])

                print(f"CSV file successfully saved at {csv_file}")

    def map_headers(self, header):
        header_count = {'Item': 0}
        mapped_header = []
        for col in header:
            if col == 'Item':
                header_count['Item'] += 1
                if header_count['Item'] == 1:
                    mapped_header.append(self.header_mapping['MB51_GR']['Item PO'])
                elif header_count['Item'] == 2:
                    mapped_header.append(self.header_mapping['MB51_GR']['Item GR'])
            else:
                mapped_header.append(self.header_mapping['MB51_GR'].get(col, col))
        return mapped_header

    def get_selected_columns(self):
        return [
            'Posting_Date', 'Material', 'Material_Description', 'Purchase_Order',
            'Document_Date', 'Qty_in_Un_of_Entry', 'Item_PO', 'Movement_Type',
            'WBS_Element', 'Unit_of_Entry', 'Item_GR', 'Amount_in_LC',
            'Material_Document', 'User_Name', 'Document_Header_Text',
            'Reference', 'Order', 'Vendor', 'Reservation', 'Batch'
        ]

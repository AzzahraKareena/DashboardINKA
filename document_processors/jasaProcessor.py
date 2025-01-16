import csv

class jasaProcessor:
    header_mapping = {
        'PROJECT DEF': 'project_def',
        'WBS_element': 'wbs_element',
        'Sales_Document': 'sales_document',
        'SO DATE': 'so_date',
        'CUSTOMER PO NUMBER': 'customer_po_number',
        'Sold-to_party': 'sold_to_party',
        'CUSTOMER NAME': 'customer_name',
        'MATERIAL CODE': 'material_code',
        'MATERIAL NAME': 'material_name',
        'NO ITEM': 'no_item',
        'QTY SO': 'qty_so',
        'UOM': 'uom',
        'UNIT PRICE SO': 'unit_price_so',
        'TOTAL PRICE SO': 'total_price_so',
        'TOTAL PRICE BILLING': 'total_price_billing',
        'SISA PRICE BILLING': 'sisa_price_billing',
        'STATUS': 'status',
    }

    @staticmethod
    def csv_to_mapped_csv(input_csv, output_csv):
        try:
            with open(input_csv, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                
                # Menulis header yang telah dipetakan ke file output
                with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
                    fieldnames = [jasaProcessor.header_mapping.get(field, field) for field in reader.fieldnames]
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()

                    # Menulis setiap baris data dengan header yang sudah dipetakan
                    for row in reader:
                        mapped_row = {jasaProcessor.header_mapping.get(k, k): v for k, v in row.items()}
                        writer.writerow(mapped_row)

            print(f"File berhasil diproses dan disimpan sebagai {output_csv}")

        except FileNotFoundError:
            print(f"File {input_csv} tidak ditemukan.")
        except Exception as e:
            print(f"Kesalahan saat mengonversi file CSV: {e}")

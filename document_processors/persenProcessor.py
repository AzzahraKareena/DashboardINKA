import csv

class persenProcessor:
    header_mapping = {
        'PROJECT DEF': 'project_def',
        'WBS_element': 'WBS_element',
        'Sales_Document': 'Sales_Document',
        'SO DATE': 'so_date',
        'CUSTOMER PO NUMBER': 'customer_po_number',
        'Sold-to_party': 'sold_to_party',
        'MATERIAL CODE': 'material_code',
        'MATERIAL NAME': 'material_name',
        'NO': 'no',
        'QTY SO': 'qty_so',
        'UOM.1': 'uom',
        'UNIT PRICE SO': 'unit_price_so',
        'TOTAL PRICE SO': 'total_price_so',
        'DELIVER QTY': 'deliver_qty',
        'UOM.1': 'uom_1',
        'UNIT PRICE DO': 'unit_price_do',
        'DELIVERED': 'delivered',
        'TO BE DELIVER QTY': 'to_be_deliver_qty',
        'INVOICED QTY': 'invoiced_qty',
        'UOM.2': 'uom_2',
        'UNIT PRICE INVOICE': 'unit_price_invoice',
        'TOTAL PRICE BILLING': 'total_price_billing',
        'TO BE INVOICED': 'to_be_invoiced',
        'PO date': 'po_date',
        'Req.dlv.dt': 'req_dlv_dt',
        'Duration (in days)': 'duration_in_days',
        'Status': 'status',
        'Persen': 'persen'
    }

    @staticmethod
    def csv_to_mapped_csv(input_csv, output_csv):
        try:
            with open(input_csv, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                
                # Menulis header yang telah dipetakan ke file output
                with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
                    fieldnames = [persenProcessor.header_mapping.get(field, field) for field in reader.fieldnames]
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()

                    # Menulis setiap baris data dengan header yang sudah dipetakan
                    for row in reader:
                        mapped_row = {persenProcessor.header_mapping.get(k, k): v for k, v in row.items()}
                        writer.writerow(mapped_row)

            print(f"File berhasil diproses dan disimpan sebagai {output_csv}")

        except FileNotFoundError:
            print(f"File {input_csv} tidak ditemukan.")
        except Exception as e:
            print(f"Kesalahan saat mengonversi file CSV: {e}")

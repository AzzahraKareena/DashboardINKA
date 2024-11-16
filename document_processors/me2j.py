from bs4 import BeautifulSoup

def process_me2j(file_path, document_id):
    # Membaca file HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Menggunakan BeautifulSoup untuk memparsing HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Mengambil data dengan penanganan kesalahan
    wbs_element = soup.find('element_for_wbs_element').get_text() if soup.find('element_for_wbs_element') else None
    purchasing_document = soup.find('element_for_purchasing_document').get_text() if soup.find('element_for_purchasing_document') else None
    item = soup.find('element_for_item').get_text() if soup.find('element_for_item') else None
    material = soup.find('element_for_material').get_text() if soup.find('element_for_material') else None
    deletion_indicator = soup.find('element_for_deletion_indicator').get_text() if soup.find('element_for_deletion_indicator') else None
    short_text = soup.find('element_for_short_text').get_text() if soup.find('element_for_short_text') else None
    order_quantity = soup.find('element_for_order_quantity').get_text() if soup.find('element_for_order_quantity') else None
    order_unit = soup.find('element_for_order_unit').get_text() if soup.find('element_for_order_unit') else None
    document_date = soup.find('element_for_document_date').get_text() if soup.find('element_for_document_date') else None
    vendor_supplying_plant = soup.find('element_for_vendor_supplying_plant').get_text() if soup.find('element_for_vendor_supplying_plant') else None
    still_to_be_delivered_value = soup.find('element_for_still_to_be_delivered_value').get_text() if soup.find('element_for_still_to_be_delivered_value') else None
    still_to_be_invoiced_qty = soup.find('element_for_still_to_be_invoiced_qty').get_text() if soup.find('element_for_still_to_be_invoiced_qty') else None
    still_to_be_invoiced_val = soup.find('element_for_still_to_be_invoiced_val').get_text() if soup.find('element_for_still_to_be_invoiced_val') else None
    net_price = soup.find('element_for_net_price').get_text() if soup.find('element_for_net_price') else None
    still_to_be_delivered_qty = soup.find('element_for_still_to_be_delivered_qty').get_text() if soup.find('element_for_still_to_be_delivered_qty') else None
    currency = soup.find('element_for_currency').get_text() if soup.find('element_for_currency') else None
    acct_assignment_cat = soup.find('element_for_acct_assignment_cat').get_text() if soup.find('element_for_acct_assignment_cat') else None
    po_history_release_documentation = soup.find('element_for_po_history_release_documentation').get_text() if soup.find('element_for_po_history_release_documentation') else None

    # Cek apakah data yang diperlukan tidak None
    if any(v is None for v in [
        wbs_element, purchasing_document, item, material, deletion_indicator,
        short_text, order_quantity, order_unit, document_date, vendor_supplying_plant,
        still_to_be_delivered_value, still_to_be_invoiced_qty, still_to_be_invoiced_val,
        net_price, still_to_be_delivered_qty, currency, acct_assignment_cat,
        po_history_release_documentation
    ]):
        raise ValueError("One or more required fields are missing in the uploaded document.")

    # Kembalikan data yang diekstrak
    return (wbs_element, purchasing_document, item, material, deletion_indicator,
            short_text, order_quantity, order_unit, document_date, vendor_supplying_plant,
            still_to_be_delivered_value, still_to_be_invoiced_qty, still_to_be_invoiced_val,
            net_price, still_to_be_delivered_qty, currency, acct_assignment_cat,
            po_history_release_documentation)

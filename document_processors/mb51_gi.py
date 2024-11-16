from bs4 import BeautifulSoup

def process_mb51_gi(file_path, document_id):
    # Membaca file HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Menggunakan BeautifulSoup untuk memparsing HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Mengambil data dengan penanganan kesalahan
    posting_date = soup.find('element_for_posting_date').get_text() if soup.find('element_for_posting_date') else None
    material = soup.find('element_for_material').get_text() if soup.find('element_for_material') else None
    material_description = soup.find('element_for_material_description').get_text() if soup.find('element_for_material_description') else None
    purchase_order = soup.find('element_for_purchase_order').get_text() if soup.find('element_for_purchase_order') else None
    document_date = soup.find('element_for_document_date').get_text() if soup.find('element_for_document_date') else None
    qty_in_unit_of_entry = soup.find('element_for_qty_in_unit_of_entry').get_text() if soup.find('element_for_qty_in_unit_of_entry') else None
    item = soup.find('element_for_item').get_text() if soup.find('element_for_item') else None
    movement_type = soup.find('element_for_movement_type').get_text() if soup.find('element_for_movement_type') else None
    wbs_element = soup.find('element_for_wbs_element').get_text() if soup.find('element_for_wbs_element') else None
    unit_of_entry = soup.find('element_for_unit_of_entry').get_text() if soup.find('element_for_unit_of_entry') else None
    amount_in_lc = soup.find('element_for_amount_in_lc').get_text() if soup.find('element_for_amount_in_lc') else None
    material_document = soup.find('element_for_material_document').get_text() if soup.find('element_for_material_document') else None
    user_name = soup.find('element_for_user_name').get_text() if soup.find('element_for_user_name') else None
    document_header_text = soup.find('element_for_document_header_text').get_text() if soup.find('element_for_document_header_text') else None
    reference = soup.find('element_for_reference').get_text() if soup.find('element_for_reference') else None
    order = soup.find('element_for_order').get_text() if soup.find('element_for_order') else None
    vendor = soup.find('element_for_vendor').get_text() if soup.find('element_for_vendor') else None
    reservation = soup.find('element_for_reservation').get_text() if soup.find('element_for_reservation') else None
    batch = soup.find('element_for_batch').get_text() if soup.find('element_for_batch') else None

    # Cek apakah data yang diperlukan tidak None
    if any(v is None for v in [
        posting_date, material, material_description, purchase_order, document_date,
        qty_in_unit_of_entry, item, movement_type, wbs_element, unit_of_entry,
        amount_in_lc, material_document, user_name, document_header_text, reference,
        order, vendor, reservation, batch
    ]):
        raise ValueError("One or more required fields are missing in the uploaded document.")

    # Kembalikan data yang diekstrak
    return (posting_date, material, material_description, purchase_order, document_date,
            qty_in_unit_of_entry, item, movement_type, wbs_element, unit_of_entry,
            amount_in_lc, material_document, user_name, document_header_text, reference,
            order, vendor, reservation, batch)

from bs4 import BeautifulSoup

def process_me5j(file_path, document_id):
    # Membaca file HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Menggunakan BeautifulSoup untuk memparsing HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Mengambil data dengan penanganan kesalahan
    wbs_element = soup.find('element_for_wbs_element').get_text() if soup.find('element_for_wbs_element') else None
    purchase_requisition = soup.find('element_for_purchase_requisition').get_text() if soup.find('element_for_purchase_requisition') else None
    item_of_requisition = soup.find('element_for_item_of_requisition').get_text() if soup.find('element_for_item_of_requisition') else None
    requisition_date = soup.find('element_for_requisition_date').get_text() if soup.find('element_for_requisition_date') else None
    deliv_date = soup.find('element_for_deliv_date').get_text() if soup.find('element_for_deliv_date') else None
    deletion_indicator = soup.find('element_for_deletion_indicator').get_text() if soup.find('element_for_deletion_indicator') else None
    processing_status = soup.find('element_for_processing_status').get_text() if soup.find('element_for_processing_status') else None
    material = soup.find('element_for_material').get_text() if soup.find('element_for_material') else None
    short_text = soup.find('element_for_short_text').get_text() if soup.find('element_for_short_text') else None
    material_group = soup.find('element_for_material_group').get_text() if soup.find('element_for_material_group') else None
    requisitioner = soup.find('element_for_requisitioner').get_text() if soup.find('element_for_requisitioner') else None
    purchasing_group = soup.find('element_for_purchasing_group').get_text() if soup.find('element_for_purchasing_group') else None
    quantity_requested = soup.find('element_for_quantity_requested').get_text() if soup.find('element_for_quantity_requested') else None
    unit_of_measure = soup.find('element_for_unit_of_measure').get_text() if soup.find('element_for_unit_of_measure') else None
    purchase_order = soup.find('element_for_purchase_order').get_text() if soup.find('element_for_purchase_order') else None
    purchase_order_date = soup.find('element_for_purchase_order_date').get_text() if soup.find('element_for_purchase_order_date') else None
    purchase_order_item = soup.find('element_for_purchase_order_item').get_text() if soup.find('element_for_purchase_order_item') else None
    quantity_ordered = soup.find('element_for_quantity_ordered').get_text() if soup.find('element_for_quantity_ordered') else None
    document_type = soup.find('element_for_document_type').get_text() if soup.find('element_for_document_type') else None
    storage_location = soup.find('element_for_storage_location').get_text() if soup.find('element_for_storage_location') else None

    # Cek apakah data yang diperlukan tidak None
    if any(v is None for v in [
        wbs_element, purchase_requisition, item_of_requisition, requisition_date, deliv_date,
        deletion_indicator, processing_status, material, short_text, material_group,
        requisitioner, purchasing_group, quantity_requested, unit_of_measure,
        purchase_order, purchase_order_date, purchase_order_item, quantity_ordered,
        document_type, storage_location
    ]):
        raise ValueError("One or more required fields are missing in the uploaded document.")

    # Kembalikan data yang diekstrak
    return (wbs_element, purchase_requisition, item_of_requisition, requisition_date, deliv_date,
            deletion_indicator, processing_status, material, short_text, material_group,
            requisitioner, purchasing_group, quantity_requested, unit_of_measure,
            purchase_order, purchase_order_date, purchase_order_item, quantity_ordered,
            document_type, storage_location)

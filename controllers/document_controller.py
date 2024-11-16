from flask import Blueprint, request, jsonify, flash, redirect, url_for, send_file, render_template
import os
from werkzeug.utils import secure_filename  # Impor secure_filename dari werkzeug
from models.document import DocumentModel
from document_processors.mb52 import MB52Processor



from document_processors.mb51_gi import process_mb51_gi 
from document_processors.mb52 import MB52Processor


document_bp = Blueprint('document', __name__)

# @document_bp.route('/upload_mb51_gr', methods=['GET', 'POST'])
# def upload_mb51_gr():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and file.filename.endswith('.MHTML'):
#             # Save the uploaded file to the uploads directory
#             mhtml_folder = 'uploads/mhtml'
#             if not os.path.exists(mhtml_folder):
#                 os.makedirs(mhtml_folder)
#             mhtml_file_path = os.path.join(mhtml_folder, file.filename)
#             file.save(mhtml_file_path)

#             # Prepare CSV output path
#             csv_folder = 'uploads/csv'
#             if not os.path.exists(csv_folder):
#                 os.makedirs(csv_folder)
#             output_csv = os.path.join(csv_folder, file.filename.replace('.MHTML', '.csv'))

#             # Process the MHTML file
#             process_mb51_gr(mhtml_file_path, output_csv)
#             return "File processed successfully!"
#     return render_template('mb51_gr_upload.html')

class DocumentController:
    def __init__(self):
        self.model = DocumentModel()

    def upload_file(self, file, doc_type):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads/', filename)  # Pastikan folder uploads ada
            file.save(file_path)
            document_id = self.model.insert_document(filename, doc_type)

            # Panggil pemrosesan berdasarkan jenis dokumen
            if doc_type == 'CN42N':
                self.process_cn42n(file_path, document_id)
            elif doc_type == 'CN43N':
                self.process_cn43n(file_path, document_id)

            return document_id
        else:
            raise ValueError("File type not allowed")

    def save_file(self, file, subfolder):
        """Save file to specified subfolder under 'uploads/'."""
        folder_path = os.path.join('uploads', subfolder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, secure_filename(file.filename))
        file.save(file_path)
        return file_path

    
    
    def allowed_file(self, filename):
        allowed_extensions = {'htm', 'html', 'mhtml'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

   

   
    

        
    def process_mb51_gi(self, file_path, document_id):
        try:
            (posting_date, material, material_description, purchase_order, document_date,
             qty_in_unit_of_entry, item, movement_type, wbs_element, unit_of_entry,
             amount_in_lc, material_document, user_name, document_header_text, reference,
             order, vendor, reservation, batch) = process_mb51_gi(file_path, document_id)
            self.model.insert_mb51_gi_data(posting_date, material, material_description, purchase_order,
                                            document_date, qty_in_unit_of_entry, item, movement_type,
                                            wbs_element, unit_of_entry, amount_in_lc, material_document,
                                            user_name, document_header_text, reference, order,
                                            vendor, reservation, batch)
        except ValueError as e:
            flash(str(e))
    
    def process_mb52(self, file_path, document_id):
            try:
                # Assuming the MB52 processor has a method for processing the file
                self.mb52_processor.insert_mb52_data(file_path, document_id)
            except ValueError as e:
                flash(str(e))

    # In your DocumentController class

    def upload_mb52(self):
        if request.method == 'POST':
            file = request.files.get('file')
            
            # Call the existing upload logic
            if file and file.filename.endswith('.html'):
                file_path = os.path.join('uploads/', secure_filename(file.filename))
                file.save(file_path)

                # Insert the document entry in the Document table
                document_id = self.model.insert_document(file.filename, 'MB52')  # Adjust the doc_type as needed

                # Process the MB52 file
                self.process_mb52(file_path, document_id)
                flash('MB52 file uploaded and data inserted successfully!', 'success')
                return redirect(url_for('upload_mb52'))  # Redirect after success
            else:
                flash('Invalid file type. Please upload a .html file.', 'error')
        
        return render_template('upload_mb52.html')  # Render the upload form



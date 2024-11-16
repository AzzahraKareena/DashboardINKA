from flask import render_template, request
from models.mb51_gr_model import MB51GRModel
from document_processors.mb51_gr import MB51GRProcessor
import os

class MB51GRController:
    def __init__(self):
        self.model = MB51GRModel()
        self.processor = MB51GRProcessor()

    def upload_mb51_gr(self):
        if request.method == 'POST':
            file = request.files.get('file')
            if not file:
                return render_template('error.html', message="No file selected."), 400

            try:
                # Define paths for the uploaded file and output CSV
                mhtml_file_path = os.path.join('uploads/mhtml', file.filename)
                output_csv_path = os.path.join('uploads/csv', file.filename.replace('.MHTML', '.csv').replace('.mhtml', '.csv'))
                
                # Save the uploaded file
                file.save(mhtml_file_path)
                
                # Process the MHTML file and save as CSV
                self.processor.mhtml_to_csv(mhtml_file_path, output_csv_path)

                # Save data to the database
                selected_columns = self.processor.get_selected_columns()
                self.model.save_to_database(output_csv_path, selected_columns)

                # Render the success page on successful processing
                return render_template('success.html', message="File processed and data saved to the database.")
            except Exception as e:
                # Render the error page if an exception occurs
                return render_template('error.html', message=str(e)), 500

        # Render the upload page for GET requests
        return render_template('upload_mb51_gr.html')

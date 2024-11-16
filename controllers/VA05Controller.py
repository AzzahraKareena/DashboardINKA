import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from models.VA05Model import process_va05_data

va05_blueprint = Blueprint('va05', __name__)

@va05_blueprint.route('/va05/upload', methods=['GET', 'POST'])
def upload_va05():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file:
            return render_template('error.html', message="No file provided."), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        try:
            process_va05_data(file_path)
            return render_template('success.html', message="File telah masuk ke dalam database.")
        except Exception as e:
            return render_template('error.html', message=str(e)), 500

    return render_template('upload.html')


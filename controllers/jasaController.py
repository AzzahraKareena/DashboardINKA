import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from models.jasaModel import process_jasa_data
jasa_blueprint = Blueprint('jasa', __name__)

@jasa_blueprint.route('/jasa/upload', methods=['GET', 'POST'])
def upload_jasa():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file:
            return render_template('error.html', message="No file provided."), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        try:
            process_jasa_data(file_path)
            return render_template('success.html', message="File telah masuk ke dalam database.")
        except Exception as e:
            return render_template('error.html', message=str(e)), 500

    return render_template('upload.html')
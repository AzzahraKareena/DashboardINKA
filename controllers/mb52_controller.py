import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from models.mb52_model import process_mb52_data

mb52_blueprint = Blueprint('mb52', __name__)

@mb52_blueprint.route('/mb52/upload', methods=['GET', 'POST'])
def upload_mb52():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file:
            return render_template('error.html', message="No file provided."), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        try:
            process_mb52_data(file_path)
            return render_template('success.html', message="MB52 data processed and stored in the database.")
        except Exception as e:
            return render_template('error.html', message=str(e)), 500

    return render_template('upload.html')

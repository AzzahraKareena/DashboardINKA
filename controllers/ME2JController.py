import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from models.ME2JModel import process_me2j_data
me2j_blueprint = Blueprint('me2j', __name__)

@me2j_blueprint.route('/me2j/upload', methods=['GET', 'POST'])
def upload_me2j():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file:
            return render_template('error.html', message="No file provided."), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        try:
            process_me2j_data(file_path)
            return render_template('success.html', message="File telah masuk ke dalam database.")
        except Exception as e:
            return render_template('error.html', message=str(e)), 500

    return render_template('upload.html')
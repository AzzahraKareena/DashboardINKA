import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from models.MB51GIModel import process_mb51_gi_data  # Updated import statement

mb51_gi_blueprint = Blueprint('mb51_gi', __name__)  # Updated blueprint name

@mb51_gi_blueprint.route('/mb51_gi/upload', methods=['GET', 'POST'])  # Updated route
def upload_mb51_gi():  # Updated function name
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file:
            return render_template('error.html', message="No file provided."), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        try:
            process_mb51_gi_data(file_path)
            return render_template('success.html', message="File telah masuk ke dalam database.")
        except Exception as e:
            return render_template('error.html', message=str(e)), 500

    return render_template('upload.html')
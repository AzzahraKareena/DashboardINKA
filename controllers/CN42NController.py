from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from models.CN42NModel import process_cn42n_data

cn42n_blueprint = Blueprint('cn42n', __name__)

@cn42n_blueprint.route('/cn42n/upload', methods=['POST'])
def upload_cn42n():
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({"message": "No file provided.", "status": "error"}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        process_cn42n_data(file_path)
        return jsonify({"message": "File telah masuk ke dalam database.", "status": "success"}), 200
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500

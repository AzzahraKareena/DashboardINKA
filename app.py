from flask import Flask, render_template, request,Blueprint, redirect, url_for, flash, jsonify
import os
from collections import OrderedDict
import json
import mysql.connector
from werkzeug.utils import secure_filename
from controllers.document_controller import DocumentController
from controllers.mb52_controller import mb52_blueprint
from controllers.MATSPECController import matspec_blueprint
from controllers.mb51_controller import MB51GRController
from controllers.CN42NController import cn42n_blueprint
from controllers.CN43NController import cn43n_blueprint
from controllers.CN55NController import cn55n_blueprint
from controllers.VA05Controller import va05_blueprint
from controllers.ME5JController import me5j_blueprint
from controllers.ME2JController import me2j_blueprint
from controllers.MB51_GIController import mb51_gi_blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Database configuration
db_config = {
    'host': '36.94.112.123',       # atau '127.0.0.1' jika server lokal
    'user': 'it',            # ganti dengan user database kamu
    'password': 'ITIMS321',            # ganti dengan password yang sesuai
    'database': 'dashboard',   # ganti dengan nama database kamu
    'port': 3306               # port default MySQL
}
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
# matspec_controller = MatspecController(db_config)

# Configuration for upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'htm', 'html', 'mhtml'}
# mb51_gr_blueprint = Blueprint('mb51_gr', __name__) 

# Create instances of controllers
document_controller = DocumentController()
# app.register_blueprint(mb51_gr_blueprint)
app.register_blueprint(cn42n_blueprint)
app.register_blueprint(cn43n_blueprint)  # Register the CN43N blueprint
app.register_blueprint(cn55n_blueprint)
app.register_blueprint(va05_blueprint)
app.register_blueprint(me5j_blueprint)
app.register_blueprint(me2j_blueprint)
app.register_blueprint(mb51_gi_blueprint)
app.register_blueprint(mb52_blueprint)
# app.register_blueprint(mb51_gr_blueprint)
# app.register_blueprint(matspec_blueprint, url_prefix='/matspec')
app.register_blueprint(matspec_blueprint)
mb51_gr_controller = MB51GRController()

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the main upload page
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle uploading CN42N documents
@app.route('/upload/cn42n', methods=['GET', 'POST'])
def upload_cn42n():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                cn42n_blueprint.upload_cn42n(mhtml_file_path)
                flash('CN42N file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_cn42n'))
            except Exception as e:
                flash(f"Error processing CN42N file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_cn42n.html')

# Route to handle uploading CN43N documents
@app.route('/upload/cn43n', methods=['GET', 'POST'])
def upload_cn43n():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                cn43n_blueprint.upload_cn43n(mhtml_file_path)
                flash('CN43N file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_cn43n'))
            except Exception as e:
                flash(f"Error processing CN43N file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_cn43n.html')

# Route to handle uploading CN55N documents
@app.route('/upload/cn55n', methods=['GET', 'POST'])
def upload_cn55n():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                cn55n_blueprint.upload_cn55n(mhtml_file_path)
                flash('CN55N file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_cn55n'))
            except Exception as e:
                flash(f"Error processing CN55N file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_cn55n.html')

# Route to handle uploading VA05 documents
@app.route('/upload/va05', methods=['GET', 'POST'])
def upload_va05():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                va05_blueprint.upload_va05(mhtml_file_path)
                flash('VA05 file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_va05'))
            except Exception as e:
                flash(f"Error processing VA05 file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_va05.html')

# Route to handle uploading ME5J documents
@app.route('/upload/me5j', methods=['GET', 'POST'])
def upload_me5j():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                me5j_blueprint.upload_me5j(mhtml_file_path)
                flash('ME5J file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_me5j'))
            except Exception as e:
                flash(f"Error processing ME5J file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_me5j.html')

# Route to handle uploading ME2J documents
@app.route('/upload/me2j', methods=['GET', 'POST'])
def upload_me2j():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                me2j_blueprint.upload_me2j(mhtml_file_path)
                flash('ME2J file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_me2j'))
            except Exception as e:
                flash(f"Error processing ME2J file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_me2j.html')

# Route to handle uploading MB51_GI documents
@app.route('/upload/mb51_gi', methods=['GET', 'POST'])
def upload_mb51_gi():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                mb51_gi_blueprint.upload_mb51_gi(mhtml_file_path)
                flash('MB51_GI file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_mb51_gi'))
            except Exception as e:
                flash(f"Error processing MB51_GI file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_mb51_gi.html')

# Route to handle uploading ME2J documents
@app.route('/upload/matspec', methods=['GET', 'POST'])
def upload_matspec():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                matspec_blueprint.upload_matspec(mhtml_file_path)
                flash('MATSPEC file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_matspec'))
            except Exception as e:
                flash(f"Error processing MATSPEC file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_matspec.html')

# Route to handle uploading MB51_GR documents
@app.route('/upload/mb51_gr', methods=['GET', 'POST'])
def upload_mb51_gr():
    return mb51_gr_controller.upload_mb51_gr()

## Route to handle uploading MB51_GI documents
# @app.route('/upload/mb51_gr', methods=['GET', 'POST'])
# def upload_mb51_gr():
#     if request.method == 'POST':
#         file = request.files['file']
        
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(mhtml_file_path)

#             try:
#                 mb51_gr_blueprint.upload_mb51_gr(mhtml_file_path)
#                 flash('MB51_GR file uploaded and processed successfully!', 'success')
#                 return redirect(url_for('upload_mb51_gr'))
#             except Exception as e:
#                 flash(f"Error processing MB51_GR file: {str(e)}", 'error')
#                 print(f"Exception occurred: {str(e)}")  # For debugging purposes
#         else:
#             flash('No file selected or unsupported file type.', 'error')
        
#     return render_template('upload_mb51_gr.html')

# # Route for uploading MB52 documents
# @app.route('/upload/mb52', methods=['GET', 'POST'])
# def upload_mb52():
#     return document_controller.upload_mb52()

# Route to handle uploading ME2J documents
@app.route('/upload/mb52', methods=['GET', 'POST'])
def upload_mb52():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                mb52_blueprint.upload_mb52(mhtml_file_path)
                flash('MB52 file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_mb52'))
            except Exception as e:
                flash(f"Error processing MB52 file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_mB52.html')


# # Inisialisasi controller
# matspec_controller = MatspecController(db_config)

# # Route untuk mengunggah dokumen matspec
# @app.route('/matspec/upload', methods=['GET', 'POST'])
# def upload_matspec():
#     if request.method == 'POST':
#         file = request.files.get('file')
#         if file:
#             # Tentukan path untuk menyimpan file yang diunggah
#             mhtml_file_path = os.path.join('uploads', file.filename)
#             file.save(mhtml_file_path)

#             # Tentukan path untuk output CSV dan kolom yang dipilih
#             output_csv_path = os.path.join('csv', file.filename.replace('.MHTML', '.csv').replace('.mhtml', '.csv'))
#             selected_columns = [
#                 'Material', 'Material_Description', 'Text', 'Base_Unit_of_Measure',
#                 'Material_Group', 'Material_Type', 'Plant', 'DF_at_client_level',
#                 'Valuation_Class', 'Created_by', 'Last_Change', 'Price'
#             ]

#             # Proses file menggunakan controller
#             result = matspec_controller.process_matspec_file(mhtml_file_path, output_csv_path, 'matspec', selected_columns)

#             # Render halaman berdasarkan hasil pemrosesan
#             if result["status"] == "success":
#                 return render_template('success.html', message=result["message"])
#             else:
#                 return render_template('error.html', message=result["message"])

#         # Jika tidak ada file yang diunggah
#         return render_template('upload_matspec.html', message="No file selected.")
    
#     # Tampilkan halaman upload jika metode adalah GET
#     return render_template('upload_matspec.html')

# Fungsi untuk mengambil data dari tabel cn42n
@app.route('/api/cn42n', methods=['GET'])
def get_cn42n():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT `Project definition`, `Name` FROM cn42n")
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel cn43n
@app.route('/api/cn43n', methods=['GET'])
def get_cn43n():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT `Project definition`, `WBS element`, `Name`, `Level`, `Status` FROM cn43n")
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel cn55n
@app.route('/api/cn55n', methods=['GET'])
def get_cn55n():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT `Project definition`, `WBS Element`, `Sales Document`, `Sales Document Item` FROM cn55n")
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel va05
@app.route('/api/va05', methods=['GET'])
def get_va05():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `Sales Document`, `Sales Document Type`, `Document Date`, 
                   `Purchase order number`, `Status`, `Item (SD)`, `Description`, 
                   `Material`, `Confirmed Quantity`, `Delivery Date`, `Created by`, 
                   `Sold-to party`, `Name 1`, `Exchange Rate`, `Order Quantity`, 
                   `Base Unit of Measure`, `Net price`, `Pricing unit`, 
                   `Unit of measure`, `Pricing date`, `Net Value`, 
                   `Document Currency`, `Goods Issue Date`, `Created on` 
            FROM va05
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel me5j
@app.route('/api/me5j', methods=['GET'])
def get_me5j():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `WBS Element`, `Purchase Requisition`, `Item of Requisition`, 
                   `Requisition Date`, `Deliv. date(From/to)`, `Deletion Indicator`, 
                   `Processing status`, `Material`, `Short Text`, `Material Group`, 
                   `Requisitioner`, `Purchasing Group`, `Quantity Requested`, 
                   `Unit of Measure`, `Purchase Order`, `Purchase Order Date`, 
                   `Purchase Order Item`, `Quantity Ordered`, `Document Type`, 
                   `Storage Location`
            FROM me5j
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel me2j
@app.route('/api/me2j', methods=['GET'])
def get_me2j():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `WBS Element`, `Purchasing Document`, `Item`, `Material`, 
                   `Deletion Indicator`, `Short Text`, `Order Quantity`, `Order Unit`, 
                   `Document Date`, `Vendor/supplying plant`, `Still to be delivered (value)`, 
                   `Still to be invoiced (qty)`, `Still to be invoiced (val.)`, `Net price`, 
                   `Still to be delivered (qty)`, `Currency`, `Acct Assignment Cat.`, 
                   `PO history/release documentation` 
            FROM me2j
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel mb51_gr
@app.route('/api/mb51_gr', methods=['GET'])
def get_mb51_gr():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `Posting Date`, `Material`, `Material Description`, `Purchase Order`, 
                   `Document Date`, `Qty in Un. of Entry`, `Item PO`, `Movement Type`, 
                   `WBS Element`, `Unit of Entry`,`Item GR`,`Amount in LC`, `Material Document`, 
                   `User Name`, `Document Header Text`, `Reference`, `Order`, 
                   `Vendor`, `Reservation`, `Batch`
            FROM mb51_gr
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel mb51_gi
@app.route('/api/mb51_gi', methods=['GET'])
def get_mb51_gi():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `Posting Date`, `Material`, `Material Description`, `Purchase Order`, 
                   `Document Date`, `Qty in Un. of Entry`, `Item`, `Movement Type`, 
                   `WBS Element`, `Unit of Entry`, `Amount in LC`, `Material Document`, 
                   `User Name`, `Document Header Text`, `Reference`, `Order`, 
                   `Vendor`, `Reservation`, `Batch`
            FROM mb51_gi
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel mb52
@app.route('/api/mb52', methods=['GET'])
def get_mb52():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `Material`, `Plnt`, `SLoc`, `S`, `Special stock number`, 
                   `BUn`, `Unrestricted`, `Crcy`, `Value Unrestricted` 
            FROM mb52
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel matspec
@app.route('/api/matspec', methods=['GET'])
def get_matspec():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT `Material`, `Material Description`, `Text`, 
                   `Base Unit of Measure`, `Material Group`, `Material Type`, 
                   `Plant`, `DF at client level`, `Valuation Class`, 
                   `Created by`, `Last Change`, `Price` 
            FROM matspec
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)

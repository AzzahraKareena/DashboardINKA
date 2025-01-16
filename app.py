from flask import Flask, render_template, request,Blueprint, redirect, url_for, flash, jsonify
import os
from collections import OrderedDict
import json
import mysql.connector
from werkzeug.utils import secure_filename
from controllers.mb52_controller import mb52_blueprint
from controllers.MATSPECController import matspec_blueprint
from controllers.mb51_controller import MB51GRController
from controllers.CN42NController import cn42n_blueprint
from controllers.CN43NController import cn43n_blueprint
from controllers.CN55NController import cn55n_blueprint
from controllers.VA05Controller import va05_blueprint
from controllers.ME5JController import me5j_blueprint
from controllers.ME2JController import me2j_blueprint
from controllers.ME5AController import me5a_blueprint
from controllers.MB51_GIController import mb51_gi_blueprint
from controllers.barangController import barang_blueprint
from controllers.jasaController import jasa_blueprint
from controllers.persenController import persen_blueprint
from controllers.auth_controller import auth_blueprint
from controllers.kategori_controller import kategori_blueprint


app = Flask(__name__)
app.secret_key = 'your_secret_key'



# Database configuration
db_config = {
        'host': '36.94.112.125',
        'user': 'it_dev',
        'password': 'MyPassword1!',  # Ubah jika ada password
        'database': 'dashboard',
        'port': '3306',
       
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

app.register_blueprint(auth_blueprint, url_prefix='/auth')
# app.register_blueprint(mb51_gr_blueprint)
app.register_blueprint(cn42n_blueprint)
app.register_blueprint(cn43n_blueprint)  # Register the CN43N blueprint
app.register_blueprint(cn55n_blueprint)
app.register_blueprint(va05_blueprint)
app.register_blueprint(me5j_blueprint)
app.register_blueprint(me2j_blueprint)
app.register_blueprint(mb51_gi_blueprint)
app.register_blueprint(mb52_blueprint)
app.register_blueprint(me5a_blueprint)
app.register_blueprint(barang_blueprint)
app.register_blueprint(jasa_blueprint)
app.register_blueprint(persen_blueprint)
# app.register_blueprint(mb51_gr_blueprint)
# app.register_blueprint(matspec_blueprint, url_prefix='/matspec')
app.register_blueprint(matspec_blueprint)
mb51_gr_controller = MB51GRController()
app.register_blueprint(kategori_blueprint)



# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the main upload page
@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@app.route('/kategori')
def kategori_index():
    return render_template('kategori/index.html')

@app.route('/web')
def web():
    return render_template('web.html')

@app.route('/kategori/create')
def kategori_create():
    return render_template('kategori/create.html')

@app.route('/kategori/edit/<int:id>')
def kategori_edit(id):
    return render_template('kategori/edit.html')


@app.route('/users', methods=['GET'])
def show_users():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch all users from the database
    cursor.execute("SELECT * FROM users")  # Assuming the table is named 'users'
    users = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    # Pass the users data to the template
    return render_template('add_user.html', users=users)

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

# Rute untuk halaman upload dan tabel
@app.route('/cn42n', methods=['GET'])
def cn42n_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Ambil data dari tabel CN42N
        cursor.execute("SELECT `Project_definition`, `Name` FROM CN42N LIMIT 10")
        data = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    
    # Render template dengan data dari database
    return render_template('upload_cn42n.html', data=data)

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

# Route to handle uploading ME2J documents
@app.route('/upload/me5a', methods=['GET', 'POST'])
def upload_me5a():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                me2j_blueprint.upload_me5a(mhtml_file_path)
                flash('ME2J file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_me5a'))
            except Exception as e:
                flash(f"Error processing ME5A file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_me5a.html')

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

# Route to handle uploading  documents
@app.route('/upload/barang', methods=['GET', 'POST'])
def upload_barang():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                barang_blueprint.upload_barang(mhtml_file_path)
                flash('barang file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_barang'))
            except Exception as e:
                flash(f"Error processing barang file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_barang.html')


@app.route('/upload/jasa', methods=['GET', 'POST'])
def upload_jasa():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                jasa_blueprint.upload_jasa(mhtml_file_path)
                flash('jasa file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_jasa'))
            except Exception as e:
                flash(f"Error processing jasa file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_jasa.html')

# Route to handle uploading ME2J documents
@app.route('/upload/persen', methods=['GET', 'POST'])
def upload_persen():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mhtml_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(mhtml_file_path)

            try:
                persen_blueprint.upload_persen(mhtml_file_path)
                flash('persen file uploaded and processed successfully!', 'success')
                return redirect(url_for('upload_persen'))
            except Exception as e:
                flash(f"Error processing persen file: {str(e)}", 'error')
                print(f"Exception occurred: {str(e)}")  # For debugging purposes
        else:
            flash('No file selected or unsupported file type.', 'error')
        
    return render_template('upload_persen.html')


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
        cursor.execute("SELECT `Project_definition`, `Name` FROM cn42n")
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
        cursor.execute("SELECT `Project_definition`, `WBS_element`, `Name`, `Level`, `Status` FROM cn43n")
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
        cursor.execute("SELECT `Project_definition`, `WBS_Element`, `Sales_Document`, `Sales_Document_Item` FROM cn55n")
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
            SELECT `Sales_Document`, `Sales_Document_Type`, `Document_Date`, 
                   `Purchase_order_number`, `Status`, `Item_(SD)`, `Description`, 
                   `Material`, `Confirmed_Quantity`, `Delivery_Date`, `Created_by`, 
                   `Sold-to_party`, `Name_1`, `Exchange_Rate`, `Order_Quantity`, 
                   `Base_Unit_of_Measure`, `Net_price`, `Pricing_unit`, 
                   `Unit_of_measure`, `Pricing_date`, `Net_Value`, 
                   `Document_Currency`, `Goods_Issue_Date`, `Created_on` 
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
            SELECT `WBS_Element`, `Purchase_Requisition`, `Item_of_Requisition`, 
                   `Requisition_Date`, `Deliv.date(From/to)`, `Deletion_Indicator`, 
                   `Processing_status`, `Material`, `Short_Text`, `Material_Group`, 
                   `Requisitioner`, `Purchasing_Group`, `Quantity_Requested`, 
                   `Unit_of_Measure`, `Purchase_Order`, `Purchase_Order_Date`, 
                   `Purchase_Order_Item`, `Quantity_Ordered`, `Document_Type`, 
                   `Storage_Location`
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
            SELECT `WBS_Element`, `Purchase_Order`, `Item`, `Material`, 
                   `Deletion_Indicator`, `Short_Text`, `Order_Quantity`, `Order_Unit`, 
                   `Document_Date`, `Vendor/supplying_plant`, `Still_to_be_delivered_(value)`, 
                   `Still_to_be_invoiced_(qty)`, `Still_to_be_invoiced_(val.)`, `Net_price`, 
                   `Still_to_be_delivered_(qty)`, `Currency`, `Acct_Assignment_Cat.`, 
                   `PO_history/release_documentation` 
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
            SELECT `Posting_Date`, `Material`, `Material_Description`, `Purchase_Order`, 
                   `Document_Date`, `Qty_in_Un_of_Entry`, `Item_PO`, `Movement_Type`, 
                   `WBS_Element`, `Unit_of_Entry`,`Item_GR`,`Amount_in_LC`, `Material_Document`, 
                   `User_Name`, `Document_Header_Text`, `Reference`, `Order`, 
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
            SELECT `Posting_Date`, `Material`, `Material_Description`, `Purchase_Order`, `Document_Date`, 
            `Qty_in_Un_of_Entry`, `Item`, `Movement_Type`, `WBS_Element`, `Unit_of_Entry`, `Amount_in_LC`, 
            `Material_Document`, `User_Name`, `Document_Header_Text`, `Reference`, `Order`, `Vendor`, `Reservation`, `Batch`
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
            SELECT `Material`, `Plnt`, `SLoc`, `S`, `WBS_Element`, 
                   `BUn`, `Unrestricted`, `Crcy`, `Value_Unrestricted` 
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
            SELECT `Material`, `Material_Description`, `Text`, `Base_Unit_of_Measure`, `Material_Group`, `Material_Type`, 
            `Plant`, `DF_at_client_level`, `Valuation_Class`, `Created_by`, `Last_Change`, `Price` 
            FROM matspec
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel matspec
@app.route('/api/me5a', methods=['GET'])
def get_me5a():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT acct_assignment_cat, requisitioner, purchase_requisition, 
                        req_tracking_number, item_of_requisition, release_indicator, 
                        requisition_date, release_date, changed_on, deliv_date, deletion_indicator, processing_status, 
                        material, short_text, unit_of_measure, material_group, 
                        purchasing_group, closed
            FROM me5a
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel matspec
@app.route('/api/barang', methods=['GET'])
def get_barang():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT project_def, wbs_element, so_document,so_date, req_delivery_date,duration, customer_po_number, customer_code, customer_name, 
            material_code, material_name, no, qty_so, uom, unit_price_so, total_price_so, deliver_qty, 
            uom_1, unit_price_do, total_price_do, to_be_deliver_qty, invoiced_qty, uom_2, unit_price_billing, 
            total_price_billing, to_be_invoice, status, 
            unit_price_invoice, to_be_deliver_invoice
        FROM barang;

        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk mengambil data dari tabel matspec
@app.route('/api/jasa', methods=['GET'])
def get_jasa():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT project_def, wbs_element, sales_document, so_date, customer_po_number,
                    sold_to_party,customer_name, material_code, material_name, no_item, qty_so, uom,
                    unit_price_so, total_price_so, total_price_billing, sisa_price_billing, status
            FROM jasa
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/report')
def report():
    return render_template('report.html')


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)

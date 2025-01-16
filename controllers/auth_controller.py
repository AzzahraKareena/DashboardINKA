from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import UserModel
from utils.decorators import admin_required

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.get_user_by_username(username)

        if user and check_password_hash(user['password'], password):
            # Simpan informasi pengguna ke dalam session
            session['user_id'] = user['id']
            session['role'] = user['role']  # Pastikan role dari database
            session['username'] = user['username']
        
            # Redirect berdasarkan role
            if user['role'] == 'admin':
                return redirect(url_for('upload'))  # Halaman untuk admin
            else:
                return redirect(url_for('web'))  # Halaman untuk user
        else:
            flash('Invalid username or password.', 'error')

    return render_template('landing_page.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nip = request.form.get('nip')
        divisi = request.form.get('divisi')

        # Cek apakah sudah ada admin di database
        admin_exists = UserModel.check_if_admin_exists()

        # Jika tidak ada admin, role otomatis 'admin', jika ada, role 'user'
        role = 'admin' if not admin_exists else 'user'

        if UserModel.get_user_by_username(username) or UserModel.get_user_by_email(email):
            flash('Username or email already exists', 'error')
            return redirect(url_for('auth.register'))  # Kembali ke halaman register jika ada kesalahan
        else:
            hashed_password = generate_password_hash(password)
            UserModel.create_user(username, email, hashed_password, nip, divisi, role)
            flash(f'Account created successfully as {role}', 'success')
            return redirect(url_for('auth.login'))  # Arahkan ke halaman login setelah pendaftaran berhasil

    return render_template('register.html')  # Tampilkan halaman register jika permintaan adalah GET


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return render_template('landing_page.html')


@auth_blueprint.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    users = UserModel.get_all_users()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nip = request.form['nip']
        divisi = request.form['divisi']
        role = request.form['role']
        hashed_password = generate_password_hash(password)
        UserModel.create_user(username, email, hashed_password, nip, divisi, role)
        flash('User  added successfully!', 'success')
    return render_template('add_user.html', users=users)

@auth_blueprint.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = UserModel.get_user_by_id(user_id)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        nip = request.form['nip']
        divisi = request.form['divisi']
        role = request.form['role']
        UserModel.update_user(user_id, username, email, nip, divisi, role)
        flash('User  updated successfully!', 'success')
        return redirect(url_for('show_users'))
    return render_template('edit_user.html', user=user)

@auth_blueprint.route('/admin/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    UserModel.delete_user(user_id)
    flash('User  deleted successfully!', 'success')
    return redirect(url_for('show_users'))
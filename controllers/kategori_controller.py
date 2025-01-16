from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.kategoriModel import KategoriModel
from models.user import UserModel
from utils.decorators import admin_required

kategori_blueprint = Blueprint('kategori', __name__, url_prefix='/kategori')

@kategori_blueprint.route('/')
@admin_required
def index():
    kategoris = KategoriModel.get_all_kategori()
    return render_template('kategori/index.html', kategoris=kategoris)

@kategori_blueprint.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        nama_kategori = request.form['nama_kategori']
        divisi = request.form['divisi']
        KategoriModel.create_kategori(nama_kategori, divisi)
        return redirect(url_for('kategori.index'))
    divisis = UserModel.get_all_users()
    return render_template('kategori/create.html', divisis=divisis)

@kategori_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit(id):
    kategori = KategoriModel.get_kategori_by_id(id)
    if kategori is None:
        flash('Kategori tidak ditemukan', 'error')
        return redirect(url_for('kategori.index'))

    if request.method == 'POST':
        nama_kategori = request.form['nama_kategori']
        divisi = request.form['divisi']
        KategoriModel.update_kategori(id, nama_kategori, divisi)
        return redirect(url_for('kategori.index'))

    return render_template('kategori/edit.html', kategori=kategori)

@kategori_blueprint.route('/delete/<int:id>')
@admin_required
def delete(id):
    KategoriModel.delete_kategori(id)
    return redirect(url_for('kategori.index'))
import mysql.connector

class KategoriModel:
    db_config = {
        'host': '36.94.112.125',
        'user': 'it_dev',
        'password': 'MyPassword1!',  # Ubah jika ada password
        'database': 'dashboard',
        'port': '3306',
       
    }

    @staticmethod
    def _get_connection():
        return mysql.connector.connect(**KategoriModel.db_config)

    @staticmethod
    def get_kategori_by_id(kategori_id):
        connection = KategoriModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM kategori_dashboard WHERE id = %s", (kategori_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_kategori(nama_kategori, divisi):
        connection = KategoriModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO kategori_dashboard (nama_kategori, divisi) VALUES (%s, %s)",
                (nama_kategori, divisi),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_kategori():
        connection = KategoriModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM kategori_dashboard")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
            
    @staticmethod
    def update_kategori(kategori_id, nama_kategori, divisi):
        connection = KategoriModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE kategori_dashboard SET nama_kategori = %s, divisi = %s WHERE id = %s",
                (nama_kategori, divisi, kategori_id),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_kategori(kategori_id):
        connection = KategoriModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM kategori_dashboard WHERE id = %s", (kategori_id,))
            connection.commit()
        finally:
            cursor.close()
            connection.close()
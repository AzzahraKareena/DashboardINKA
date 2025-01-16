import mysql.connector

class UserModel:
    db_config = {
       'host': '36.94.112.125',
        'user': 'it_dev',
        'password': 'MyPassword1!',  # Ubah jika ada password
        'database': 'dashboard',
        'port': '3306',
       
    }

    @staticmethod
    def _get_connection():
        return mysql.connector.connect(**UserModel.db_config)

    @staticmethod
    def get_user_by_username(username):
        connection = UserModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_user(username, email, password, nip, divisi, role='user'):
        connection = UserModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, nip, divisi, role) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, email, password, nip, divisi, role),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_users():
        connection = UserModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def check_if_admin_exists():
        connection = UserModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS admin_count FROM users WHERE role = 'admin'")
            result = cursor.fetchone()
            return result['admin_count'] > 0
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create_user(username, email, password, nip, divisi, role='user'):
        connection = UserModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, nip, divisi, role) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, email, password, nip, divisi, role),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_user_by_email(email):
        """Mendapatkan user berdasarkan email."""
        connection = UserModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
            connection.close()
            
    @staticmethod
    def get_user_by_id(user_id):
        connection = UserModel._get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_user(user_id, username, email, nip, divisi, role):
        connection = UserModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE users SET username = %s, email = %s, nip = %s, divisi = %s, role = %s WHERE id = %s",
                (username, email, nip, divisi, role, user_id),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_user(user_id):
        connection = UserModel._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
        finally:
            cursor.close()
            connection.close()


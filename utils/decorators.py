from functools import wraps
from flask import redirect, url_for, session

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

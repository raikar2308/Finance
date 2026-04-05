from functools import wraps
from flask import session, redirect, url_for, flash


# ==============================
# LOGIN REQUIRED (ALL USERS)
# ==============================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "error")
            return redirect(url_for("admin_login.admin_login"))
        return f(*args, **kwargs)
    return wrapper


# ==============================
# ROLE REQUIRED (FLEXIBLE)
# ==============================
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:
                flash("Please login first", "error")
                return redirect(url_for("admin_login.admin_login"))

            user_role = session.get("role")

            if user_role not in roles:
                flash("Access denied", "error")
                return redirect(url_for("admin_dashboard.dashboard"))

            return f(*args, **kwargs)

        return wrapper
    return decorator
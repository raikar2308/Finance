from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from database import execute_fetchall, execute_fetchone, execute_update
from extensions import bcrypt, mail
from utils.auth import login_required, role_required
from flask_mail import Message
import secrets
import string

user_bp = Blueprint("users", __name__, url_prefix="/admin/users")


# LIST USERS

@user_bp.route("/")
@login_required
@role_required("admin")
def list_users():
    users = execute_fetchall("""
        SELECT id, email, role, status, created_at
        FROM users
        WHERE deleted_at IS NULL
        ORDER BY id DESC
    """)
    return render_template("admin/user.html", users=users)



# PASSWORD GENERATOR

def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "@#$_"
    return ''.join(secrets.choice(chars) for _ in range(length))


# ADD USER

@user_bp.route("/add", methods=["POST"])
@login_required
@role_required("admin")
def add_user():
    email = request.form.get("email")
    role = request.form.get("role")

    if not email or not role:
        flash("Email and role required", "error")
        return redirect(url_for("users.list_users"))

    #  Generate password
    plain_password = generate_password()
    password_hash = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    # Insert user
    execute_update("""
        INSERT INTO users (email, password_hash, role, status, created_at)
        VALUES (%s, %s, %s, 'ACTIVE', NOW())
    """, (email, password_hash, role))

    # Send email
    try:
        msg = Message(
            subject="Your Finance Account",
            recipients=[email]
        )

        msg.body = f"""
Hello,

Your account has been created.

Email: {email}
Password: {plain_password}

Please login and change your password.

Regards,
Finance Team
        """

        mail.send(msg)

    except Exception as e:
        print("Mail error:", e)
        flash("User created but email failed", "error")
        return redirect(url_for("users.list_users"))

    flash("User created & email sent", "success")
    return redirect(url_for("users.list_users"))




# UPDATE USER
@user_bp.route("/update/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def update_user(user_id):
    email = request.form.get("email")
    role = request.form.get("role")

    if not email or not role:
        flash("Email and role required", "error")
        return redirect(url_for("users.edit_user", user_id=user_id))

    execute_update("""
        UPDATE users
        SET email=%s, role=%s
        WHERE id=%s
    """, (email, role, user_id))

    flash("User updated successfully", "success")
    return redirect(url_for("users.list_users"))


# TOGGLE STATUS

@user_bp.route("/toggle/<int:user_id>")
@login_required
@role_required("admin")
def toggle_status(user_id):
    user = execute_fetchone("SELECT status FROM users WHERE id=%s", (user_id,))

    new_status = "BLOCKED" if user["status"] == "ACTIVE" else "ACTIVE"

    execute_update("""
        UPDATE users
        SET status=%s
        WHERE id=%s
    """, (new_status, user_id))

    flash("User status updated", "success")
    return redirect(url_for("users.list_users"))



# DELETE (SOFT)

@user_bp.route("/delete/<int:user_id>")
@login_required
@role_required("admin")
def delete_user(user_id):
    execute_update("""
        UPDATE users
        SET deleted_at=%s
        WHERE id=%s
    """, (datetime.now(), user_id))

    flash("User deleted", "success")
    return redirect(url_for("users.list_users"))



# EDIT USER PAGE

@user_bp.route("/edit/<int:user_id>")
@login_required
@role_required("admin")
def edit_user(user_id):
    user = execute_fetchone("""
        SELECT id, email, role, status
        FROM users
        WHERE id=%s AND deleted_at IS NULL
    """, (user_id,))

    return render_template("admin/edit_user.html", user=user)

@user_bp.route("/api/check-email")
def check_email():
    email = request.args.get("email")

    user = execute_fetchone("SELECT id FROM users WHERE email=%s", (email,))

    return {
        "available": False if user else True
    }
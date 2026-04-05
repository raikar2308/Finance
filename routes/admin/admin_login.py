from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from database import execute_fetchone, execute_update
from extensions import bcrypt


admin_login_bp = Blueprint("admin_login", __name__)

MAX_FAILED_ATTEMPTS = 5
LOCK_TIME_MINUTES = 15


# ADMIN LOGIN

@admin_login_bp.route("/", methods=["GET", "POST"])
def admin_login():


    #  HANDLE RESET PASSWORD

    if session.get("force_password_reset") and request.method == "POST":

        if request.args.get("skip") == "1":
            session.pop("force_password_reset", None)
            return redirect(url_for("admin_dashboard.dashboard"))

        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not new_password or new_password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("admin/admin_login.html", reset_mode=True)

        password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

        execute_update("""
            UPDATE users SET password_hash=%s WHERE id=%s
        """, (password_hash, session["user_id"]))

        session.pop("force_password_reset", None)

        flash("Password updated successfully", "success")
        return redirect(url_for("admin_dashboard.dashboard"))


    #  NORMAL LOGIN

    if request.method == "POST":

        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()

            if not email or not password:
                flash("All fields are required", "error")
                return redirect(url_for("admin_login.admin_login"))

            user = execute_fetchone(
                "SELECT * FROM users WHERE email=%s AND deleted_at IS NULL",
                (email,)
            )

            if not user:
                flash("Invalid credentials", "error")
                return redirect(url_for("admin_login.admin_login"))

            if user["role"] not in ["admin", "analyst", "viewer"]:
                flash("Invalid role", "error")
                return redirect(url_for("admin_login.admin_login"))

            if user["status"] != "ACTIVE":
                flash("Account is blocked", "error")
                return redirect(url_for("admin_login.admin_login"))

            #  PASSWORD CHECK
            if not bcrypt.check_password_hash(user["password_hash"], password):
                flash("Invalid credentials", "error")
                return redirect(url_for("admin_login.admin_login"))

            #  SUCCESS LOGIN
            execute_update("""
                UPDATE users 
                SET failed_attempts=0,
                    last_login=NOW()
                WHERE id=%s
            """, (user["id"],))

            session.clear()
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            #  DEFAULT PASSWORD FLOW
            if user["role"] in ["analyst", "viewer"] and user["last_login"] is None:
                session["force_password_reset"] = True
                return render_template("admin/admin_login.html", reset_mode=True)

            return redirect(url_for("admin_dashboard.dashboard"))

        except Exception as e:
            print("Login error:", e)
            flash("Server error", "error")
            return redirect(url_for("admin_login.admin_login"))

    return render_template("admin/admin_login.html")




# LOGOUT

@admin_login_bp.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("admin_login.admin_login"))


@admin_login_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "user_id" not in session:
        return redirect(url_for("admin_login.admin_login"))

    if request.method == "POST":

        new_password = request.form.get("password")

        if not new_password:
            flash("Password required", "error")
            return redirect(url_for("admin_login.reset_password"))

        password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

        execute_update("""
            UPDATE users
            SET password_hash=%s
            WHERE id=%s
        """, (password_hash, session["user_id"]))

        session.pop("force_password_reset", None)

        flash("Password updated successfully", "success")
        return redirect(url_for("admin_dashboard.dashboard"))

    return render_template("admin/reset_password.html")


@admin_login_bp.route("/skip-password")
def skip_password():

    session.pop("force_password_reset", None)

    flash("You can update password later from profile", "info")
    return redirect(url_for("admin_dashboard.dashboard"))
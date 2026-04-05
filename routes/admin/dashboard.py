from flask import Blueprint, render_template, redirect, url_for, session
from database import execute_fetchone, execute_fetchall
from utils.auth import login_required, role_required

dashboard_bp = Blueprint("admin_dashboard", __name__, url_prefix="/admin/dashboard")


@dashboard_bp.route("/")
@login_required
@role_required("admin", "analyst", "viewer")
def dashboard():


    if session.get("force_password_reset"):
        return redirect(url_for("admin_login.reset_password"))


    # DASHBOARD LOGIC


    # TOTALS
    totals = execute_fetchone("""
        SELECT
            SUM(CASE WHEN type='INCOME' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) AS total_expense
        FROM financial_records
        WHERE deleted_at IS NULL
    """)

    total_income = totals["total_income"] or 0
    total_expense = totals["total_expense"] or 0
    balance = total_income - total_expense

    # CATEGORY WISE
    categories = execute_fetchall("""
        SELECT category, SUM(amount) as total
        FROM financial_records
        WHERE deleted_at IS NULL
        GROUP BY category
        ORDER BY total DESC
        LIMIT 5
    """)

    # RECENT RECORDS
    recent = execute_fetchall("""
        SELECT *
        FROM financial_records
        WHERE deleted_at IS NULL
        ORDER BY record_date DESC
        LIMIT 5
    """)

    #  MONTHLY TREND
    monthly = execute_fetchall("""
        SELECT
            DATE_FORMAT(record_date, '%Y-%m') as month,
            SUM(CASE WHEN type='INCOME' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) as expense
        FROM financial_records
        WHERE deleted_at IS NULL
        GROUP BY month
        ORDER BY month
    """)

    return render_template(
        "admin/dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        categories=categories,
        recent=recent,
        monthly=monthly
    )
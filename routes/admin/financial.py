from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from database import execute_fetchall, execute_fetchone, execute_update
from utils.auth import role_required, login_required

financial_bp = Blueprint("financial", __name__, url_prefix="/admin/financial")

# LIST RECORDS + FILTER

@financial_bp.route("/")
@login_required
@role_required("admin", "analyst")
def list_records():
    type_filter = request.args.get("type")
    category = request.args.get("category")

    query = """
        SELECT * FROM financial_records
        WHERE deleted_at IS NULL
    """
    params = []

    if type_filter:
        query += " AND type=%s"
        params.append(type_filter)

    if category:
        query += " AND category=%s"
        params.append(category)

    query += " ORDER BY id DESC"

    records = execute_fetchall(query, tuple(params))
    return render_template("admin/financial.html", records=records)


# ADD RECORD

@financial_bp.route("/add", methods=["POST"])
@login_required
@role_required("admin", "analyst")
def add_record():
    amount = request.form.get("amount")
    type_ = request.form.get("type")
    category = request.form.get("category")
    date = request.form.get("record_date")
    notes = request.form.get("notes")

    if not amount or not type_ or not category or not date:
        flash("All required fields must be filled", "error")
        return redirect(url_for("financial.list_records"))

    execute_update("""
        INSERT INTO financial_records (amount, type, category, record_date, notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (amount, type_, category, date, notes))

    flash("Record added successfully", "success")
    return redirect(url_for("financial.list_records"))


# UPDATE RECORD

@financial_bp.route("/update/<int:id>", methods=["POST"])
@login_required
@role_required("admin", "analyst")
def update_record(id):
    execute_update("""
        UPDATE financial_records
        SET amount=%s, type=%s, category=%s, record_date=%s, notes=%s, updated_at=NOW()
        WHERE id=%s
    """, (
        request.form["amount"],
        request.form["type"],
        request.form["category"],
        request.form["record_date"],
        request.form["notes"],
        id
    ))

    flash("Record updated", "success")
    return redirect(url_for("financial.list_records"))


# DELETE (SOFT)

@financial_bp.route("/delete/<int:id>")
@login_required
@role_required("admin")
def delete_record(id):
    execute_update("""
        UPDATE financial_records
        SET deleted_at=%s
        WHERE id=%s
    """, (datetime.now(), id))

    flash("Record deleted", "success")
    return redirect(url_for("financial.list_records"))
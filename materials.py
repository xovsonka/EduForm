from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from db import get_connection, get_categories
from utils.utils import generate_tags_from_text
import os
from utils.utils import login_required
from utils.utils import get_file_hash
from io import BytesIO
import hashlib
import pdfkit
from werkzeug.utils import secure_filename
from pptx import Presentation
from psycopg2.extras import RealDictCursor
import psycopg2.errors
from pptx import Presentation
from pptx.util import Inches, Pt
from bs4 import BeautifulSoup
from psycopg2.extras import RealDictCursor
import re
from bs4 import BeautifulSoup
from pptx import Presentation
from pptx.dml.color import RGBColor
import re
from utils.utils import html_text_to_pptx
materials_bp = Blueprint("materials", __name__)
from flask_babel import _  
from flask import jsonify
from db import get_focuses, get_grades
from utils.utils import load_focuses_translated,load_grades_translated
@materials_bp.route("/materials", methods=["GET"])
@login_required
def materials():
    query = request.args.get("query", "")
    file_type = request.args.get("type", "")
    category = request.args.get("category", "")
    focus = request.args.get("focus", "")
    grade = request.args.get("grade", "")

    filtered = bool(query or file_type or category or focus or grade)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT DISTINCT m.*, c.name AS category_name,
                        f.name AS focus_name,
                        g.name AS grade_name
        FROM materials m
        LEFT JOIN categories c ON m.category_id = c.id
        LEFT JOIN focuses f ON m.focus_id = f.id
        LEFT JOIN grades g ON m.grade_id = g.id
        LEFT JOIN material_tags mt ON m.id = mt.material_id
        LEFT JOIN tags t ON mt.tag_id = t.id
        WHERE TRUE
    """
    params = []

    if query:
        sql += " AND (t.name ILIKE %s OR m.title ILIKE %s OR m.description ILIKE %s)"
        like = f"%{query}%"
        params.extend([like, like, like])

    if file_type:
        sql += " AND m.file_path ILIKE %s"
        params.append(f"%.{file_type}")

    if category:
        sql += " AND c.id = %s"
        params.append(int(category))

    if focus:
        sql += " AND f.id = %s"
        params.append(int(focus))

    if grade:
        sql += " AND g.id = %s"
        params.append(int(grade))

    sql += " ORDER BY m.created_at DESC"

    if not filtered:
        sql += " LIMIT 4"

    cur.execute(sql, tuple(params))
    materials = cur.fetchall()

    categories = load_categories_translated()
    focuses = load_focuses_translated()
    grades = load_grades_translated()

    cur.close()
    conn.close()

    return render_template(
        "materials.html",
        materials=materials,
        categories=categories,
        focuses=focuses,  
        grades=grades,  
        filtered=filtered
    )

@materials_bp.route("/materials/add", methods=["POST"])
@login_required
def add_material():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    category_id = request.form.get("category_id")
    focus_id = request.form.get("focus_id")  
    grade_id = request.form.get("grade_id")  
    file = request.files.get("file")

    errors = []

    if not title or len(title) < 3:
        errors.append(_("❗ Názov musí mať aspoň 3 znaky."))

    if not description or len(description) < 10:
        errors.append(_("❗ Popis musí mať aspoň 10 znakov."))

    if not file or file.filename == '':
        errors.append(_("❗ Je potrebné nahrať súbor."))
    else:
        allowed_mime_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ]
        
        if file.mimetype not in allowed_mime_types:
            errors.append(_("❌ Nepodporovaný formát súboru. Povolené sú len PDF a PPTX."))

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        max_size = 10 * 1024 * 1024  
        if file_size > max_size:
            errors.append(_("⚠️ Súbor je príliš veľký (maximálna veľkosť je 10MB)."))

    
    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for("materials.materials"))

    filename = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "materials")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    file_bytes = file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    file.stream.seek(0)
    file.save(file_path)

    relative_path = os.path.relpath(file_path, "static").replace("\\", "/")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        
        cur.execute("SELECT id FROM materials WHERE file_hash = %s", (file_hash,))
        if cur.fetchone():
            flash(_("⚠️ Materiál s rovnakým obsahom už existuje."), "warning")
            return redirect(url_for("materials.materials"))

        
        cur.execute("""
            INSERT INTO materials (title, description, category_id, file_path, user_id, file_hash, focus_id, grade_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            title,
            description,
            category_id,
            f"uploads/materials/{filename}",
            session["user_id"],
            file_hash,
            focus_id or None, 
            grade_id or None   
        ))

        conn.commit()
        flash(_("✅ Materiál bol úspešne pridaný."), "success")

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flash(_("⚠️ Tento materiál už existuje v databáze."), "warning")

    except Exception as e:
        conn.rollback()
        flash(_("🛠️ Chyba databázy: ") + str(e), "danger")

    finally:
        cur.close()
        conn.close()

    return redirect(url_for("materials.materials"))

@materials_bp.route("/materials/filter", methods=["GET"])
@login_required
def filter_materials():
    query      = request.args.get("query", "")
    file_type  = request.args.get("type", "")
    category   = request.args.get("category", "")
    focus      = request.args.get("focus", "")
    grade      = request.args.get("grade", "")
    only_mine  = request.args.get("only_mine") 
    page       = int(request.args.get("page", 1))

    per_page   = 6
    real_limit = per_page + 1
    offset     = (page - 1) * per_page

    conn = get_connection()
    cur  = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT DISTINCT m.*, 
               c.name AS category_name,
               f.code AS focus_code,
               g.code AS grade_code
        FROM materials m
        LEFT JOIN categories    c ON c.id  = m.category_id
        LEFT JOIN focuses       f ON f.id  = m.focus_id
        LEFT JOIN grades        g ON g.id  = m.grade_id
        LEFT JOIN material_tags mt ON mt.material_id = m.id
        LEFT JOIN tags          t ON t.id  = mt.tag_id
        WHERE TRUE
    """
    params = []

    if query:
        sql += """
            AND (t.name ILIKE %s
              OR m.title       ILIKE %s
              OR m.description ILIKE %s)
        """
        like = f"%{query}%"
        params.extend([like, like, like])

    if file_type:
        sql += " AND m.file_path ILIKE %s"
        params.append(f"%.{file_type}")

    if category:
        sql += " AND c.id = %s"
        params.append(int(category))

    if focus:
        sql += " AND m.focus_id = %s"
        params.append(int(focus))

    if grade:
        sql += " AND m.grade_id = %s"
        params.append(int(grade))

    
    if only_mine == "1":
        sql += " AND m.user_id = %s"
        params.append(session["user_id"])

    sql += " ORDER BY m.created_at DESC LIMIT %s OFFSET %s"
    params.extend([real_limit, offset])

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    
    materials = []
    for row in rows[:per_page]:
        row["focus_label"] = _(row["focus_code"]) if row.get("focus_code") else None
        row["grade_label"] = _(row["grade_code"]) if row.get("grade_code") else None
        materials.append(row)

    has_more = len(rows) > per_page

    return jsonify({
        "html": render_template("partials/_materials_items.html", materials=materials),
        "has_more": has_more
    })


from utils.utils import html_text_to_pdf, html_text_to_pptx,validate_inputs,load_categories_translated,pptx_to_html_text


from flask_babel import gettext as _
@materials_bp.route("/materials/add-ai", methods=["POST"])
@login_required
def add_ai_material():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    category_id = request.form.get("category_id")
    focus_id = request.form.get("focus_id") or None
    grade_id = request.form.get("grade_id") or None
    content = request.form.get("content", "").strip()
    material_type = request.form.get("material_type")

    errors = []
    if not title or len(title) < 3:
        errors.append(_("Názov musí mať aspoň 3 znaky."))
    if not content:
        errors.append(_("Obsah je povinný."))
    if not category_id:
        errors.append(_("Musíte vybrať kategóriu."))

    if errors:
        for err in errors:
            flash(f"❗ {err}", "danger")

        categories = load_categories_translated()
        return render_template(
            "ai_generate.html",
            generated=content,
            topic=title,
            level=category_id,
            material_type=material_type,
            categories=categories
        )

    extension = "pptx" if material_type == "Prezentácia" else "pdf"
    filename = secure_filename(f"{title}.{extension}")
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "materials")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    try:
        if material_type == "Prezentácia":
            html_text_to_pptx(title, content, file_path)
        else:
            html_text_to_pdf(content, output_path=file_path)
    except Exception as e:
        flash(_("❌ Chyba pri generovaní súboru: ") + str(e), "danger")
        return redirect(url_for("ai.generate"))

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    db_path = f"uploads/materials/{filename}"

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM materials WHERE file_hash = %s", (file_hash,))
        if cur.fetchone():
            flash(_("⚠️ Materiál s rovnakým obsahom už existuje."), "warning")
            return redirect(url_for("materials.materials"))

        cur.execute("""
            INSERT INTO materials (title, description, category_id, focus_id, grade_id, file_path, user_id, file_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, description, category_id, focus_id, grade_id, db_path, session["user_id"], file_hash))

        conn.commit()
        flash(_("✅ AI materiál bol uložený."), "success")

    except Exception as e:
        conn.rollback()
        flash(_("❌ DB chyba: ") + str(e), "danger")

    finally:
        cur.close()
        conn.close()

    return redirect(url_for("materials.materials"))




from utils.utils import extract_text_from_pdf, extract_text_from_pptx

from utils.utils import extract_text_from_pdf, extract_text_from_pptx,html_text_to_pdf,html_text_to_pptx,pdf_to_html_text,pptx_to_html_text
@materials_bp.route("/materials/edit/<int:material_id>", methods=["GET", "POST"])
@login_required
def edit_material(material_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM materials WHERE id = %s", (material_id,))
    material = cur.fetchone()

    if not material:
        flash(_("❗ Materiál neexistuje."), "danger")
        return redirect(url_for("materials.materials"))

    ext = material["file_path"].split('.')[-1].lower()
    full_file_path = os.path.join("static", material["file_path"])
    extracted_text = ""

    if request.method == "POST":
        if material["user_id"] != session["user_id"]:
            flash(_("❌ Nemáš oprávnenie aktualizovať tento materiál."), "danger")
            return redirect(url_for("materials.materials"))

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        new_content = request.form.get("content", "").strip()
        focus_id = request.form.get("focus_id")
        grade_id = request.form.get("grade_id")

        
        focus_id = int(focus_id) if focus_id else None
        grade_id = int(grade_id) if grade_id else None

        if not title or not new_content:
            flash(_("❗ Názov a obsah sú povinné."), "danger")
            return redirect(request.url)

        filename = secure_filename(f"{title}.{ext}")
        upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "materials")
        os.makedirs(upload_dir, exist_ok=True)
        new_file_path = os.path.join(upload_dir, filename)

        old_file_path = os.path.join("static", material["file_path"])
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

        try:
            if ext == "pdf":
                html_text_to_pdf(new_content, new_file_path)
            elif ext == "pptx":
                html_text_to_pptx(new_content, new_file_path)
            else:
                flash(_("❌ Nepodporovaný formát na úpravu."), "danger")
                return redirect(url_for("materials.materials"))
        except Exception as e:
            flash(_("❌ Chyba pri ukladaní súboru: %(error)s", error=str(e)), "danger")
            return redirect(url_for("materials.materials"))

        with open(new_file_path, "rb") as f:
            file_bytes = f.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        relative_path = os.path.relpath(new_file_path, "static").replace("\\", "/")

        cur.execute("""
            UPDATE materials
            SET title = %s, description = %s, file_path = %s, file_hash = %s, focus_id = %s, grade_id = %s
            WHERE id = %s
        """, (title, description, f"uploads/materials/{filename}", file_hash, focus_id, grade_id, material_id))

        conn.commit()
        flash(_("✅ Materiál bol úspešne aktualizovaný."), "success")
        return redirect(url_for("materials.materials"))

    else:
        if os.path.exists(full_file_path):
            try:
                if ext == "pdf":
                    extracted_text = pdf_to_html_text(full_file_path)
                elif ext == "pptx":
                    extracted_text = pptx_to_html_text(full_file_path)
                else:
                    flash(_("❌ Tento formát sa nedá upravovať."), "danger")
                    return redirect(url_for("materials.materials"))
            except Exception as e:
                flash(_("❌ Chyba pri načítavaní súboru: %(error)s", error=str(e)), "danger")
                return redirect(url_for("materials.materials"))

    cur.close()
    conn.close()
    grades = load_grades_translated()
    focuses = load_focuses_translated()
    return render_template("edit_material.html", material=material, extracted_text=extracted_text, grades=grades, focuses=focuses)



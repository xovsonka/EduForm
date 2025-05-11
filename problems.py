from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename
from db import get_connection
import os
import hashlib
from utils.utils import login_required
from utils.utils import generate_tags_from_text
from utils.utils import load_categories_translated
from flask import jsonify, render_template
from flask_babel import _  

problems_bp = Blueprint("problems", __name__, url_prefix="/problems")


@problems_bp.route("/problems", methods=["GET"])
@login_required
def problems():
    query = request.args.get("query", "")
    category = request.args.get("category", "")
    filtered = bool(query or category)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT DISTINCT p.*, c.name AS category_name
        FROM problems p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN problem_tags pt ON p.id = pt.problem_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        WHERE TRUE
    """
    params = []

    if query:
        sql += " AND (p.title ILIKE %s OR p.description ILIKE %s OR t.name ILIKE %s)"
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

    if category:
        sql += " AND c.name = %s"
        params.append(category)

    sql += " ORDER BY p.created_at DESC"
    if not filtered:
        sql += " LIMIT 4"

    cur.execute(sql, tuple(params))
    problems = cur.fetchall()

    for p in problems:
        cur.execute("""
            SELECT file_path, description
            FROM problem_solutions
            WHERE problem_id = %s
            ORDER BY created_at DESC
        """, (p["id"],))
        p["solutions"] = cur.fetchall()

    category=load_categories_translated()
    cur.close()
    conn.close()

    return render_template("problems.html", problems=problems, categories= category, filtered=filtered)



@problems_bp.route("/add", methods=["POST"])
@login_required
def add_problem():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    category_id = request.form.get("category", "")
    solution_file = request.files.get("solution_file")
    solution_description = request.form.get("solution_description", "").strip()

    errors = []
    if not title or len(title) < 3:
        errors.append(_("❗ Názov musí mať aspoň 3 znaky."))
    if not description or len(description) < 10:
        errors.append(_("❗ Popis musí mať aspoň 10 znakov."))
    if not category_id:
        errors.append(_("❗ Musíte vybrať kategóriu."))

    if solution_file:
        if not solution_file.filename.endswith(".pdf"):
            errors.append(_("❌ Riešenie musí byť vo formáte PDF."))
        if not solution_description:
            errors.append(_("❗ Musíte pridať popis riešenia."))

    if errors:
        for err in errors:
            flash(err, "danger")
        return redirect(url_for("problems.problems"))

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
            INSERT INTO problems (user_id, title, description, category_id)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (session["user_id"], title, description, category_id))
        problem_id = cur.fetchone()["id"]

        if solution_file:
            filename = secure_filename(solution_file.filename)
            upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "problems")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)

            file_bytes = solution_file.read()
            file_hash = hashlib.sha256(file_bytes).hexdigest()
            solution_file.stream.seek(0)
            solution_file.save(file_path)

            cur.execute("""
                INSERT INTO problem_solutions (problem_id, user_id, file_path, description)
                VALUES (%s, %s, %s, %s)
            """, (problem_id, session["user_id"], f"uploads/problems/{filename}", solution_description))

        tags = generate_tags_from_text(f"{title} {description}")
        for tag in tags:
            cur.execute("SELECT id FROM tags WHERE name = %s", (tag,))
            row = cur.fetchone()
            tag_id = row["id"] if row else None

            if not tag_id:
                cur.execute("INSERT INTO tags (name) VALUES (%s) RETURNING id", (tag,))
                tag_id = cur.fetchone()["id"]

            cur.execute("""
                INSERT INTO problem_tags (problem_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (problem_id, tag_id))

        conn.commit()
        flash(_("✅ Problém bol úspešne pridaný."), "success")

    except Exception as e:
        conn.rollback()
        flash(_("🛑 Chyba pri ukladaní problému: ") + str(e), "danger")

    finally:
        cur.close()
        conn.close()

    return redirect(url_for("problems.problems"))

@problems_bp.route("/filter", methods=["GET"])
@login_required
def filter_problems():
    query      = request.args.get("query", "")
    category   = request.args.get("category", "")
    only_mine  = request.args.get("only_mine") 
    page       = int(request.args.get("page", 1))

    per_page   = 6
    real_limit = per_page + 1
    offset     = (page - 1) * per_page

    conn = get_connection()
    cur  = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT DISTINCT p.*, c.name AS category_name
        FROM problems p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN problem_tags pt ON p.id = pt.problem_id
        LEFT JOIN tags t ON pt.tag_id = t.id
        WHERE TRUE
    """
    params = []

    if query:
        sql += """
            AND (
                p.title ILIKE %s
                OR p.description ILIKE %s
                OR t.name ILIKE %s
            )
        """
        like = f"%{query}%"
        params.extend([like, like, like])

    if category:
        sql += " AND c.id = %s"
        params.append(category)

    if only_mine == "1":  
        sql += " AND p.user_id = %s"
        params.append(session["user_id"])

    sql += " ORDER BY p.created_at DESC LIMIT %s OFFSET %s"
    params.extend([real_limit, offset])

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()

    problems = rows[:per_page]
    has_more = len(rows) > per_page

    for p in problems:
        cur.execute("""
            SELECT file_path, description
            FROM problem_solutions
            WHERE problem_id = %s
            ORDER BY created_at DESC
        """, (p["id"],))
        p["solutions"] = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "html": render_template(
            "partials/_problems_item.html",
            problems=problems
        ),
        "has_more": has_more
    })


@problems_bp.route("/add-solution", methods=["POST"])
@login_required
def add_solution():
    problem_id = request.form.get("problem_id")
    description = request.form.get("description", "").strip()
    file = request.files.get("solution_file")

    errors = []
    if not problem_id:
        errors.append(_("❗ Musíte vybrať problém."))
    if not file or file.filename == '':
        errors.append(_("❗ Súbor riešenia je povinný."))
    elif not file.filename.lower().endswith(".pdf"):
        errors.append(_("❌ Riešenie musí byť vo formáte PDF."))

    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for("problems.problems"))

    filename = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "problems")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    file_bytes = file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    file.stream.seek(0)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
            SELECT 1 FROM problem_solutions
            WHERE problem_id = %s AND file_hash = %s
        """, (problem_id, file_hash))

        if cur.fetchone():
            flash(_("⚠️ Riešenie s rovnakým obsahom už existuje pre tento problém."), "warning")
            return redirect(url_for("problems.problems"))

        cur.execute("SELECT user_id, title FROM problems WHERE id = %s", (problem_id,))
        problem = cur.fetchone()
        if not problem or not problem["user_id"]:
            flash(_("🛑 Nepodarilo sa nájsť autora problému."), "danger")
            return redirect(url_for("problems.problems"))

        author_id = problem["user_id"]
        problem_title = problem["title"]

        file.save(file_path)

        cur.execute("""
            INSERT INTO problem_solutions (problem_id, user_id, file_path, description, file_hash)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            problem_id,
            session["user_id"],
            f"uploads/problems/{filename}",
            description,
            file_hash
        ))

        if author_id != session["user_id"]:
            cur.execute("""
                INSERT INTO notifications (user_id, message)
                VALUES (%s, %s)
            """, (
                author_id,
                _("📥 Niekto pridal riešenie k vášmu problému: ") + problem_title
            ))


        conn.commit()
        flash(_("✅ Riešenie bolo pridané."), "success")

    except Exception as e:
        conn.rollback()
        flash(_("🛑 Chyba pri ukladaní riešenia: ") + str(e), "danger")

    finally:
        cur.close()
        conn.close()

    return redirect(url_for("problems.problems"))
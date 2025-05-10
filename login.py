from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_connection
import psycopg2.extras
from flask_babel import gettext as _

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(_("Úspešné prihlásenie!"), "success")
            return redirect(url_for("index"))
        else:
            flash(_("Nesprávne prihlasovacie údaje."), "danger")

    return render_template("login.html")


@login_bp.route("/logout")
def logout():
    lang = session.get("lang")  
    session.clear()           
    if lang:
        session["lang"] = lang 

    flash(_("Boli ste odhlásený."), "info")
    return redirect(url_for("login.login"))



@login_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash(_("Heslá sa nezhodujú."), "warning")
            return redirect(url_for("login.register"))

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if cur.fetchone():
            flash(_("Používateľské meno alebo email už existuje."), "danger")
            cur.close()
            conn.close()
            return redirect(url_for("login.register"))

        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, hashed_password))
        conn.commit()
        cur.close()
        conn.close()

        flash(_("Registrácia prebehla úspešne. Môžete sa prihlásiť."), "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")


@login_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        re_password = request.form.get("rePassword", "").strip()

        if password != re_password:
            flash(_("Heslá sa nezhodujú."), "warning")
            return redirect(url_for("login.forgot_password"))

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if not user:
            flash(_("E-mail nie je registrovaný."), "danger")
            cur.close()
            conn.close()
            return redirect(url_for("login.forgot_password"))

        hashed_password = generate_password_hash(password)

        cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, email))
        conn.commit()

        cur.close()
        conn.close()

        flash(_("Heslo bolo úspešne zmenené. Môžete sa prihlásiť."), "success")
        return redirect(url_for("login.login"))

    return render_template("forgot_password.html")

    
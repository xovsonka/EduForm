from flask import Flask, session, redirect, url_for, flash, render_template, request, g
from flask_babel import Babel, _
from dotenv import load_dotenv
import os
from datetime import timedelta 
from materials import materials_bp
from login import login_bp
from problems import problems_bp
from utils.utils import login_required
from ai import ai_bp
from flask_wtf import CSRFProtect 
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "static/uploads")
csrf = CSRFProtect(app)
app.permanent_session_lifetime = timedelta(minutes=30)

app.register_blueprint(problems_bp)
app.register_blueprint(login_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(ai_bp)

app.config['LANGUAGES'] = {
    'sk': 'Slovensky',
    'en': 'English'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'


def get_locale():
    
    if (lang := session.get("lang")) in app.config["LANGUAGES"]:
        return lang
    
    if (lang := request.args.get("lang")) in app.config["LANGUAGES"]:
        return lang

    return request.accept_languages.best_match(app.config["LANGUAGES"])


babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def inject_get_locale():
    return {'get_locale': get_locale}



@app.route("/change_lang/<lang_code>")
def change_language(lang_code):
    if lang_code in app.config["LANGUAGES"]:
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("index"))

from db import get_unread_notifications

@app.context_processor
def inject_global_notifications():
    if "user_id" in session:
        try:
            notifications = get_unread_notifications(session["user_id"])
        except Exception:
            notifications = []
    else:
        notifications = []
    return dict(notifications=notifications)


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/problems")
@login_required
def problems():
    return render_template("problems.html")

@app.route("/materials")
@login_required
def materials():
    return render_template("materials.html")


from notifications import notifications_bp
app.register_blueprint(notifications_bp)

if __name__ == "__main__":
    app.run(debug=True)


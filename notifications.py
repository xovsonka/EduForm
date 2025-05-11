from flask import Blueprint, session, jsonify
from flask_babel import _
from utils.utils import login_required
from db import get_dict_cursor 

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.route("/mark-read", methods=["POST"])
@login_required
def mark_notifications_read():
    conn,cur=get_dict_cursor()
    try:
        cur.execute(
            "UPDATE notifications SET read = TRUE WHERE user_id = %s",
            (session["user_id"],)
        )
        conn.commit()
        return jsonify(success=True)
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, error=str(e)), 500
    finally:
        cur.close()
        conn.close()

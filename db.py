import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD")
    )

def get_dict_cursor():
    conn = get_connection()
    return conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def get_categories():
    conn, cur = get_dict_cursor()
    cur.execute("SELECT * FROM categories ORDER BY name")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return categories


def get_focuses():
    conn,cur=get_dict_cursor()
    cur.execute("SELECT id, name,code FROM focuses ORDER BY name")
    focuses = cur.fetchall()
    cur.close()
    conn.close()
    return focuses

def get_grades():
    conn,cur=get_dict_cursor()
    cur.execute("SELECT id, name,code  FROM grades ORDER BY id")
    grades = cur.fetchall()
    cur.close()
    conn.close()
    return grades

def get_unread_notifications(user_id):
    conn,cur=get_dict_cursor()
    cur.execute("""
        SELECT id, message, created_at
        FROM notifications
        WHERE user_id = %s AND read = FALSE
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))
    notifications = cur.fetchall()
    cur.close()
    conn.close()
    return notifications
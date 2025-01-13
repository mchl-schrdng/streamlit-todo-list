import sqlite3
from datetime import datetime

DB_NAME = "database.db"

def calculate_metrics():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'done' AND DATE(created_at) = ?
    """, (today,))
    completed_today = cursor.fetchone()[0]
    conn.close()
    return {"completed_today": completed_today}
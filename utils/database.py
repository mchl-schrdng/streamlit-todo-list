import sqlite3
from datetime import datetime

DB_NAME = "database.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            urgency INTEGER,
            importance INTEGER,
            status TEXT DEFAULT 'created',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, description, urgency, importance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, urgency, importance)
        VALUES (?, ?, ?, ?)
    """, (title, description, urgency, importance))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, description, urgency, importance, status, created_at
        FROM tasks
    """)
    tasks = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "urgent": row[3] >= 4,
            "important": row[4] >= 4,
            "status": row[5],
            "created_at": row[6],
        }
        for row in tasks
    ]

def update_task_status(task_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ?
    """, (status, task_id))
    conn.commit()
    conn.close()
import sqlite3
from datetime import datetime

DB_NAME = "database.db"

# Initialize the database (without description)
def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            tag TEXT NOT NULL,
            urgency INTEGER,
            importance INTEGER,
            status TEXT DEFAULT 'to do',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Add a new task
def add_task(title, urgency, importance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (task, tag, urgency, importance, status)
        VALUES (?, ?, ?, 'to do')
    """, (title, urgency, importance))
    conn.commit()
    conn.close()

# Get all tasks
def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task, tag, urgency, importance, status, created_at, updated_at
        FROM tasks
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "task": row [1],
            "tag": row[2],
            "urgency": row[3],
            "importance": row[4],
            "status": row[5],
            "created_at": row[6],
            "updated_at": row[7],
        }
        for row in rows
    ]

# Update a task's status
def update_task_status(task_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, task_id))
    conn.commit()
    conn.close()

# Update task details (no description)
def update_task_details(task_id, title, urgency, importance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET task = ?, tag = ?, urgency = ?, importance = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title, urgency, importance, task_id))
    conn.commit()
    conn.close()

# Delete a task from the database
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()

# Reset the database
def reset_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()
    conn.close()
    initialize_db()
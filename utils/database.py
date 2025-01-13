import sqlite3
from datetime import datetime

DB_NAME = "database.db"

# Initialize the database
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Add a new task to the database
def add_task(title, description, urgency, importance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, urgency, importance)
        VALUES (?, ?, ?, ?)
    """, (title, description, urgency, importance))
    conn.commit()
    conn.close()

# Get all tasks from the database
def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, description, urgency, importance, status, created_at, updated_at
        FROM tasks
    """)
    tasks = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "urgency": row[3],
            "importance": row[4],
            "status": row[5],
            "created_at": row[6],
            "updated_at": row[7],
        }
        for row in tasks
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

# Update task details
def update_task_details(task_id, title, description, urgency, importance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, urgency = ?, importance = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title, description, urgency, importance, task_id))
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

def reset_database():
    """Drop the tasks table and reinitialize the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Drop the existing tasks table
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()
    conn.close()
    # Reinitialize the database
    initialize_db()
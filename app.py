import streamlit as st
import sqlite3
from utils.database import initialize_db, add_task, get_tasks, update_task_status
from utils.metrics import calculate_metrics

# Initialize the database
initialize_db()

# App layout
st.set_page_config(page_title="Streamlit To-Do List", layout="centered")
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📝 Streamlit To-Do List")

# Input Form
st.header("Add a New Task")
with st.form("task_form"):
    title = st.text_input("Task Title", placeholder="Enter your task title")
    description = st.text_area("Description", placeholder="Task details (optional)")
    urgency = st.slider("Urgency", 1, 5, 3)
    importance = st.slider("Importance", 1, 5, 3)
    submitted = st.form_submit_button("Add Task")

if submitted and title:
    add_task(title, description, urgency, importance)
    st.success("Task added successfully!")

# Quadrant Display
st.header("Task Quadrants")
tasks = get_tasks()
for quadrant, label in [
    ((True, True), "Urgent & Important"),
    ((True, False), "Urgent & Not Important"),
    ((False, True), "Not Urgent & Important"),
    ((False, False), "Not Urgent & Not Important"),
]:
    filtered = [
        task
        for task in tasks
        if task["urgent"] == quadrant[0] and task["important"] == quadrant[1]
    ]
    if filtered:
        st.subheader(label)
        for task in filtered:
            st.markdown(f"- **{task['title']}**: {task['description']}")

# Metrics
st.header("Metrics")
metrics = calculate_metrics()
st.write(f"Tasks completed today: {metrics['completed_today']}")
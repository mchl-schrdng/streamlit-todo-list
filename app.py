import streamlit as st
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
    .quadrant-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }
    .quadrant {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
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
quadrants = {
    (True, True): "Urgent & Important",
    (True, False): "Urgent & Not Important",
    (False, True): "Not Urgent & Important",
    (False, False): "Not Urgent & Not Important",
}

st.markdown('<div class="quadrant-container">', unsafe_allow_html=True)
for quadrant, label in quadrants.items():
    st.markdown(f'<div class="quadrant">', unsafe_allow_html=True)
    st.subheader(label)
    for task in tasks:
        if task["urgent"] == quadrant[0] and task["important"] == quadrant[1]:
            st.write(f"- **{task['title']}**: {task['description']}")
            if task["status"] == "created":
                if st.button(f"Mark as Done: {task['title']}", key=task["id"]):
                    update_task_status(task["id"], "done")
                    st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Task List with Filter
st.header("Task List")
selected_date = st.date_input("Filter by Creation Date")
filtered_tasks = [
    task
    for task in tasks
    if selected_date.strftime("%Y-%m-%d") in task["created_at"]
]
for task in filtered_tasks:
    st.write(f"- **{task['title']}**: {task['description']} (Status: {task['status']})")

# Metrics
st.header("Metrics")
metrics = calculate_metrics()
st.write(f"Tasks completed today: {metrics['completed_today']}")
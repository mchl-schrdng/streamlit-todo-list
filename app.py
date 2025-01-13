import streamlit as st
import pandas as pd
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

# Display Tasks in DataFrame
st.header("Task List")
tasks = get_tasks()
df_tasks = pd.DataFrame(tasks)

# Show DataFrame with Editable Status
if not df_tasks.empty:
    df_tasks["Urgency"] = df_tasks["urgent"].map({True: "High", False: "Low"})
    df_tasks["Importance"] = df_tasks["important"].map({True: "High", False: "Low"})
    df_tasks = df_tasks[["title", "description", "Urgency", "Importance", "status", "created_at"]]
    df_tasks.rename(
        columns={
            "title": "Title",
            "description": "Description",
            "status": "Status",
            "created_at": "Created At",
        },
        inplace=True,
    )
    st.dataframe(df_tasks)

    # Mark as Done Feature
    st.subheader("Mark a Task as Done")
    task_to_mark = st.selectbox("Select a Task", df_tasks[df_tasks["Status"] == "created"]["Title"])
    if st.button("Mark as Done"):
        task_id = df_tasks[df_tasks["Title"] == task_to_mark].index[0] + 1
        update_task_status(task_id, "done")
        st.success(f"Task '{task_to_mark}' marked as done!")
        st.experimental_rerun()
else:
    st.write("No tasks found.")

# Metrics
st.header("Metrics")
metrics = calculate_metrics()
st.write(f"Tasks completed today: {metrics['completed_today']}")
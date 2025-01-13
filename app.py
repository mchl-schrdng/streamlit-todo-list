import streamlit as st
import pandas as pd
from utils.database import initialize_db, add_task, get_tasks, update_task_status
from utils.metrics import calculate_metrics

# Initialize the database
initialize_db()

# App layout
st.set_page_config(
    page_title="Streamlit To-Do List",
    layout="wide",  # Enable wide mode
    initial_sidebar_state="expanded"  # Sidebar starts expanded
)

# Sidebar: Add a New Task
with st.sidebar:
    with st.form("task_form"):
        st.text_input("Task Title", placeholder="Enter your task title", key="title")
        st.text_area("Description", placeholder="Task details (optional)", key="description")
        st.slider("Urgency", 1, 5, 3, key="urgency")
        st.slider("Importance", 1, 5, 3, key="importance")
        submitted = st.form_submit_button("Add Task")

    if submitted and st.session_state.title:
        add_task(
            st.session_state.title,
            st.session_state.description,
            st.session_state.urgency,
            st.session_state.importance,
        )
        st.success("Task added successfully!")
        st.experimental_rerun()

# Main Page: Task List and Metrics
tasks = get_tasks()
if tasks:
    # Convert tasks to DataFrame
    df_tasks = pd.DataFrame(tasks)
    df_tasks["Urgency"] = df_tasks["urgent"].map({True: "High", False: "Low"})
    df_tasks["Importance"] = df_tasks["important"].map({True: "High", False: "Low"})
    df_tasks = df_tasks[["id", "title", "description", "Urgency", "Importance", "status", "created_at"]]
    df_tasks.rename(
        columns={
            "id": "Task ID",
            "title": "Title",
            "description": "Description",
            "status": "Status",
            "created_at": "Created At",
        },
        inplace=True,
    )

    # Display the tasks in a DataFrame
    st.dataframe(df_tasks, use_container_width=True)

    # Status Update Section
    task_id = st.selectbox(
        "Select Task ID to Update",
        df_tasks["Task ID"].values,
        format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
    )
    new_status = st.radio("New Status", options=["created", "done"], horizontal=True)

    if st.button("Update Status"):
        update_task_status(task_id, new_status)
        st.success(f"Task {task_id} status updated to '{new_status}'.")
        st.query_params = {"rerun": "true"}

else:
    st.write("No tasks found.")

# Metrics Section
metrics = calculate_metrics()
st.text(f"Tasks completed today: {metrics['completed_today']}")
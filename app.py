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

# Two-column layout
col1, col2 = st.columns([1.5, 2])  # Adjust column width ratio for better balance

# Left Column: Add a New Action
with col1:
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

# Right Column: Task List with Elegant Status Update
with col2:
    st.header("Task List")
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
        st.subheader("Update Task Status")
        task_id = st.selectbox(
            "Select Task ID to Update",
            df_tasks["Task ID"].values,
            format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
        )
        new_status = st.radio("New Status", options=["created", "done"], horizontal=True)

        if st.button("Update Status"):
            update_task_status(task_id, new_status)
            st.success(f"Task {task_id} status updated to '{new_status}'.")
            st.experimental_set_query_params(rerun="true")
    else:
        st.write("No tasks found.")

# Metrics Section
st.header("Metrics")
metrics = calculate_metrics()
st.write(f"Tasks completed today: {metrics['completed_today']}")

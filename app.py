import streamlit as st
import pandas as pd
from utils.database import initialize_db, add_task, get_tasks, update_task_status

# Initialize the database
initialize_db()

# App layout
st.set_page_config(
    page_title="Streamlit To-Do List",
    layout="wide",  # Enable wide mode
    initial_sidebar_state="expanded"  # Sidebar starts expanded
)

# Sidebar: Add a New Task and Update Task Status
with st.sidebar:
    # Add a New Task
    with st.container():
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

    # Update Task Status
    with st.container():
        tasks = get_tasks()
        if tasks:
            df_tasks = pd.DataFrame(tasks)
            df_tasks.rename(columns={"id": "Task ID", "title": "Title"}, inplace=True)
            task_id = st.selectbox(
                "",  # Empty label for the selectbox
                df_tasks["Task ID"].values,
                format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
            )
            new_status = st.radio("New Status", options=["created", "done"], horizontal=True)

            if st.button("Update Status"):
                update_task_status(task_id, new_status)
                st.success(f"Task {task_id} status updated to '{new_status}'.")
                st.query_params = {"rerun": "true"}
        else:
            st.write("No tasks available to update.")

# Main Page: Task List
tasks = get_tasks()
if tasks:
    st.dataframe(
        pd.DataFrame(tasks)
        .assign(
            Urgency=lambda df: df["urgent"].map({True: "High", False: "Low"}),
            Importance=lambda df: df["important"].map({True: "High", False: "Low"}),
        )
        .rename(
            columns={
                "id": "Task ID",
                "title": "Title",
                "description": "Description",
                "status": "Status",
                "created_at": "Created At",
            }
        )[["Task ID", "Title", "Description", "Urgency", "Importance", "Status", "Created At"]],
        use_container_width=True,
    )
else:
    st.write("No tasks found.")
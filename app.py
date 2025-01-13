import streamlit as st
import pandas as pd
from utils.database import initialize_db, add_task, get_tasks, update_task_status

# Initialize the database
initialize_db()

# App layout
st.set_page_config(
    page_title="todooolist",
    layout="wide",  # Enable wide mode
    initial_sidebar_state="collapsed",
    page_icon ='🤖'  # Sidebar starts expanded
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add transparency to DataFrame via CSS
st.markdown(
    """
    <style>
    [data-testid="stDataFrameContainer"] {
        background: rgba(0, 0, 0, 0.5); /* Black with 50% transparency */
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: Add a New Task and Update Task Status
with st.sidebar:
    # Add a New Task
    with st.form("task_form"):
        st.text_input("", placeholder="Enter your task title", key="title")
        st.text_area("", placeholder="Task details (optional)", key="description")
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
        # Simulate a page reload
        st.query_params = {"rerun": "true"}

# Main Page: Tasks Grouped by Status in One Column
tasks = get_tasks()
if tasks:
    # Convert tasks to a DataFrame
    df_tasks = pd.DataFrame(tasks)
    df_tasks["Urgency"] = df_tasks["urgent"].map({True: "High", False: "Low"})
    df_tasks["Importance"] = df_tasks["important"].map({True: "High", False: "Low"})
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

    # Filter tasks based on their status
    created_tasks = df_tasks[df_tasks["Status"] == "created"]
    in_progress_tasks = df_tasks[df_tasks["Status"] == "in progress"]
    pending_tasks = df_tasks[df_tasks["Status"] == "pending"]
    done_tasks = df_tasks[df_tasks["Status"] == "done"]

    # Display tasks grouped by status in one column
    st.subheader("Created Tasks")
    if not created_tasks.empty:
        st.dataframe(
            created_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
            use_container_width=True,
        )
    else:
        st.write("No created tasks.")

    st.subheader("In Progress Tasks")
    if not in_progress_tasks.empty:
        st.dataframe(
            in_progress_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
            use_container_width=True,
        )
    else:
        st.write("No tasks in progress.")

    st.subheader("Pending Tasks")
    if not pending_tasks.empty:
        st.dataframe(
            pending_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
            use_container_width=True,
        )
    else:
        st.write("No pending tasks.")

    st.subheader("Done Tasks")
    if not done_tasks.empty:
        st.dataframe(
            done_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
            use_container_width=True,
        )
    else:
        st.write("No completed tasks.")
else:
    st.write("No tasks found.")

# Sidebar: Update Task Status
with st.sidebar:
    st.subheader("Update Task Status")
    if tasks:
        with st.form("update_task_form"):
            task_id = st.selectbox(
                "Select Task ID to Update",
                df_tasks["Task ID"].values,
                format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
            )
            new_status = st.radio(
                "New Status",
                options=["pending", "in progress", "done"],  # Restricted to allowed statuses
                horizontal=True,
            )
            update_submitted = st.form_submit_button("Update Status")

        if update_submitted:
            update_task_status(task_id, new_status)
            st.success(f"Task {task_id} status updated to '{new_status}'.")
            # Refresh the page
            st.session_state["rerun"] = not st.session_state.get("rerun", False)
    else:
        st.write("No tasks available to update.")

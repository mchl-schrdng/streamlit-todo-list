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

    # Main Page: Two DataFrames for Tasks
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

    # Filter tasks into categories based on status
    created_tasks = df_tasks[df_tasks["Status"] == "created"]
    pending_tasks = df_tasks[df_tasks["Status"] == "pending"]
    in_progress_tasks = df_tasks[df_tasks["Status"] == "in progress"]
    done_tasks = df_tasks[df_tasks["Status"] == "done"]

    # Create four columns for task categories
    col1, col2 = st.columns(2)

    # Display Created and Pending Tasks in Column 1
    with col1:
        st.subheader("Created Tasks")
        if not created_tasks.empty:
            st.dataframe(
                created_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
                use_container_width=True,
            )
        else:
            st.write("No created tasks.")

        st.subheader("Pending Tasks")
        if not pending_tasks.empty:
            st.dataframe(
                pending_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
                use_container_width=True,
            )
        else:
            st.write("No pending tasks.")

    # Display In Progress and Done Tasks in Column 2
    with col2:
        st.subheader("In Progress Tasks")
        if not in_progress_tasks.empty:
            st.dataframe(
                in_progress_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
                use_container_width=True,
            )
        else:
            st.write("No in-progress tasks.")

        st.subheader("Done Tasks")
        if not done_tasks.empty:
            st.dataframe(
                done_tasks[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
                use_container_width=True,
            )
        else:
            st.write("No done tasks.")
else:
    st.write("No tasks found.")

# Sidebar: Update Task Status
tasks = get_tasks()
if tasks:
    with st.sidebar:
        st.subheader("Update Task Status")
        df_tasks = pd.DataFrame(tasks)
        df_tasks.rename(columns={"id": "Task ID", "title": "Title"}, inplace=True)
        task_id = st.selectbox(
            "Select Task to Update",
            df_tasks["Task ID"].values,
            format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
        )
        new_status = st.radio("New Status", options=["created", "pending", "in progress", "done"], horizontal=True)
        if st.button("Update Status"):
            update_task_status(task_id, new_status)
            st.success(f"Task {task_id} status updated to '{new_status}'.")
            st.experimental_rerun()

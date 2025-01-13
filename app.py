import streamlit as st
import pandas as pd
from utils.database import initialize_db, add_task, get_tasks, update_task_status, delete_task

# Initialize the database
initialize_db()

# App layout and style
st.set_page_config(
    page_title="Todooolist",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🤖"
)

# Apply global styling
st.markdown(
    """
    <style>
    /* Background gradient for the main app */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
    }
    /* Transparency and styling for dataframes */
    [data-testid="stDataFrameContainer"] {
        background: rgba(0, 0, 0, 0.5); /* Black with 50% transparency */
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for refresh
if "refresh" not in st.session_state:
    st.session_state.refresh = False

# Sidebar: Add a New Task
with st.sidebar:
    st.subheader("Add a New Task")
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
        # Trigger refresh
        st.session_state.refresh = not st.session_state.refresh

# Main Page: Tasks Grouped by Status
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

    # Task categories
    task_status_mapping = {
        "Created Tasks": df_tasks[df_tasks["Status"] == "created"],
        "In Progress Tasks": df_tasks[df_tasks["Status"] == "in progress"],
        "Pending Tasks": df_tasks[df_tasks["Status"] == "pending"],
        "Done Tasks": df_tasks[df_tasks["Status"] == "done"],
    }

    # Display tasks by category
    for status, data in task_status_mapping.items():
        st.subheader(status)
        if not data.empty:
            st.dataframe(
                data[["Task ID", "Title", "Description", "Urgency", "Importance", "Created At"]],
                use_container_width=True,
            )
        else:
            st.write(f"No {status.lower()}.")

else:
    st.write("No tasks found.")

# Sidebar: Update Task Status or Delete Task
with st.sidebar:
    st.subheader("Update or Delete Task")
    if tasks:
        with st.form("update_task_form"):
            task_id = st.selectbox(
                "Select Task ID",
                df_tasks["Task ID"].values,
                format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
            )
            new_status = st.radio(
                "New Status",
                options=["pending", "in progress", "done"],  # Restricted statuses
                horizontal=True,
            )
            update_submitted = st.form_submit_button("Update Status")
            delete_submitted = st.form_submit_button("Delete Task")  # Add delete task button

        if update_submitted:
            update_task_status(task_id, new_status)
            st.success(f"Task {task_id} status updated to '{new_status}'.")
            # Trigger refresh
            st.session_state.refresh = not st.session_state.refresh

        if delete_submitted:
            delete_task(task_id)  # Call the delete function
            st.success(f"Task {task_id} deleted successfully!")
            # Trigger refresh
            st.session_state.refresh = not st.session_state.refresh

    # Add Reset Database Option in Sidebar
    if st.sidebar.button("Reset Database"):
        reset_database()  # Call the reset function
        st.success("Database has been reset!")
        st.experimental_rerun()

    else:
        st.write("No tasks available to update or delete.")
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

    # Update Task Status
    tasks = get_tasks()
    if tasks:
        with st.form("update_task_form"):
            df_tasks = pd.DataFrame(tasks)
            df_tasks.rename(columns={"id": "Task ID", "title": "Title"}, inplace=True)
            task_id = st.selectbox(
                "",  # Empty label for the selectbox
                df_tasks["Task ID"].values,
                format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
            )
            new_status = st.radio("New Status", options=["created", "done"], horizontal=True)
            update_submitted = st.form_submit_button("Update Status")

        if update_submitted:
            update_task_status(task_id, new_status)
            st.success(f"Task {task_id} status updated to '{new_status}'.")
            # Simulate a page reload
            st.query_params = {"rerun": "true"}
    else:
        st.write("No tasks available to update.")

# Main Page: Two Columns for Tasks with Delete Feature
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

    # Filter tasks into ongoing and completed
    ongoing_tasks = df_tasks[df_tasks["Status"] == "created"]
    completed_tasks = df_tasks[df_tasks["Status"] == "done"]

    # Create two columns
    col1, col2 = st.columns(2)

    # Display Ongoing Tasks in Column 1
    with col1:
        st.subheader("Ongoing Tasks")
        if not ongoing_tasks.empty:
            for index, row in ongoing_tasks.iterrows():
                st.write(f"**{row['Title']}** - {row['Description']}")
                st.write(f"Urgency: {row['Urgency']} | Importance: {row['Importance']}")

                # Add a delete button for each task
                if st.button(f"Delete Task {row['Task ID']}", key=f"delete_ongoing_{row['Task ID']}"):
                    delete_task(row['Task ID'])  # Call the delete function
                    st.success(f"Task {row['Task ID']} deleted successfully!")
                    st.experimental_rerun()  # Reload the page after deletion
        else:
            st.write("No ongoing tasks.")

    # Display Completed Tasks in Column 2
    with col2:
        st.subheader("Completed Tasks")
        if not completed_tasks.empty:
            for index, row in completed_tasks.iterrows():
                st.write(f"**{row['Title']}** - {row['Description']}")
                st.write(f"Urgency: {row['Urgency']} | Importance: {row['Importance']}")

                # Add a delete button for each task
                if st.button(f"Delete Task {row['Task ID']}", key=f"delete_completed_{row['Task ID']}"):
                    delete_task(row['Task ID'])  # Call the delete function
                    st.success(f"Task {row['Task ID']} deleted successfully!")
                    st.experimental_rerun()  # Reload the page after deletion
        else:
            st.write("No completed tasks.")
else:
    st.write("No tasks found.")
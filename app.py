import streamlit as st
import pandas as pd
from utils.database import initialize_db, add_task, get_tasks, update_task_status, update_task_details, delete_task, reset_database

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Define a mapping function for a specific scale
def map_scale(value):
    if value == 1:
        return "Very Low"
    elif value == 2:
        return "Low"
    elif value == 3:
        return "Moderate"
    elif value == 4:
        return "High"
    elif value == 5:
        return "Very High"

# Sidebar: Add a New Task
st.sidebar.subheader("Add a New Task")
with st.sidebar.form("task_form"):
    st.text_input("Task Title", placeholder="Enter your task title", key="title", label_visibility="collapsed")
    st.text_area("Description", placeholder="Task details (optional)", key="description", label_visibility="collapsed")
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
    st.session_state.refresh = not st.session_state.get("refresh", False)  # Trigger refresh

# Main Page: Tasks Grouped by Status
tasks = get_tasks()
if tasks:
    # Convert tasks to a DataFrame
    df_tasks = pd.DataFrame(tasks)
    df_tasks["Urgency Label"] = df_tasks["urgency"].apply(map_scale)  # Apply the specific scale mapping
    df_tasks["Importance Label"] = df_tasks["importance"].apply(map_scale)  # Apply the specific scale mapping
    df_tasks.rename(
        columns={
            "id": "Task ID",
            "title": "Title",
            "description": "Description",
            "status": "Status",
            "created_at": "Created At",
            "updated_at": "Updated At",
        },
        inplace=True,
    )

    # Task categories
    task_status_mapping = {
        "To Do": df_tasks[df_tasks["Status"] == "to do"],
        "Doing": df_tasks[df_tasks["Status"] == "doing"],
        "Done": df_tasks[df_tasks["Status"] == "done"],
    }

    # Display tasks by category
    for status, data in task_status_mapping.items():
        st.subheader(status)
        if not data.empty:
            st.dataframe(
                data[["Task ID", "Title", "Description", "Urgency Label", "Importance Label", "Created At", "Updated At"]],
                use_container_width=True,
            )
        else:
            st.write(f"No {status.lower()} tasks.")
else:
    # Initialize an empty DataFrame to avoid errors
    df_tasks = pd.DataFrame(columns=["Task ID", "Title", "Description", "Urgency", "Importance", "Status", "Created At", "Updated At"])
    st.write("No tasks found.")

# Sidebar: Update Existing Task
st.sidebar.markdown("---")
st.sidebar.subheader("Update Existing Task")

# Filter out tasks with "to do" status for updates
updateable_tasks = df_tasks[df_tasks["Status"].isin(["doing", "done"])]

if not updateable_tasks.empty:
    with st.sidebar.form("update_task_form"):
        # Dropdown to select the task to update
        task_id = st.selectbox(
            "Select Task ID to Update",
            updateable_tasks["Task ID"].values,
            format_func=lambda x: f"Task {x}: {updateable_tasks[updateable_tasks['Task ID'] == x]['Title'].values[0]}",
        )

        # Fetch current values for the selected task
        selected_task = updateable_tasks[updateable_tasks["Task ID"] == task_id].iloc[0]

        # Editable fields for updating status only
        status = st.radio(
            "Status",
            options=["doing", "done"],  # Only allow "doing" and "done"
            index=["doing", "done"].index(selected_task["Status"]),
            horizontal=True,
        )

        # Submit button
        update_submitted = st.form_submit_button("Update Task")

        if update_submitted:
            # Update the task in the database
            update_task_status(task_id, status)  # Update the status
            st.success(f"Task {task_id} updated successfully!")
            st.session_state.refresh = not st.session_state.get("refresh", False)  # Trigger refresh
else:
    st.sidebar.write("No tasks available to update.")

# Sidebar: Delete Task
st.sidebar.markdown("---")
st.sidebar.subheader("Delete a Task")
if not df_tasks.empty:
    task_id_to_delete = st.sidebar.selectbox(
        "Select Task ID to Delete",
        df_tasks["Task ID"].values,
        format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
    )
    if st.sidebar.button("Delete Task"):
        delete_task(task_id_to_delete)
        st.success(f"Task {task_id_to_delete} deleted successfully!")
        st.session_state.refresh = not st.session_state.get("refresh", False)  # Trigger refresh
else:
    st.sidebar.write("No tasks available to delete.")

# Move Reset Database Option to the End of Sidebar
st.sidebar.markdown("---")
if st.sidebar.button("Reset Database (End)"):
    reset_database()
    st.success("Database has been reset!")
    st.session_state.refresh = not st.session_state.get("refresh", False)
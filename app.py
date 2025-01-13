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
    df_tasks["Urgency Label"] = df_tasks["urgency"].apply(lambda x: "High" if x >= 4 else "Low")
    df_tasks["Importance Label"] = df_tasks["importance"].apply(lambda x: "High" if x >= 4 else "Low")
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
                data[["Task ID", "Title", "Description", "Urgency Label", "Importance Label", "Created At", "Updated At"]],
                use_container_width=True,
            )
        else:
            st.write(f"No {status.lower()} tasks.")

else:
    st.write("No tasks found.")

# Sidebar: Update Existing Task
st.sidebar.subheader("Update Existing Task")
if tasks:
    with st.sidebar.form("update_task_form"):
        # Dropdown to select the task to update
        task_id = st.selectbox(
            "Select Task ID to Update",
            df_tasks["Task ID"].values,
            format_func=lambda x: f"Task {x}: {df_tasks[df_tasks['Task ID'] == x]['Title'].values[0]}",
        )

        # Fetch current values for the selected task
        selected_task = df_tasks[df_tasks["Task ID"] == task_id].iloc[0]

        # Editable fields
        title = st.text_input("Title", value=selected_task["Title"])
        description = st.text_area("Description", value=selected_task["Description"])
        urgency = st.slider("Urgency", 1, 5, int(selected_task["urgency"]))
        importance = st.slider("Importance", 1, 5, int(selected_task["importance"]))
        status = st.radio(
            "Status",
            options=["created", "pending", "in progress", "done"],
            index=["created", "pending", "in progress", "done"].index(selected_task["Status"]),
            horizontal=True,
        )

        # Submit button
        update_submitted = st.form_submit_button("Update Task")

        if update_submitted:
            # Update the task in the database
            update_task_status(task_id, status)  # Update the status
            update_task_details(
                task_id, title, description, urgency, importance
            )  # Update other details
            st.success(f"Task {task_id} updated successfully!")
            st.session_state.refresh = not st.session_state.get("refresh", False)  # Trigger refresh

    # Sidebar: Delete Task
    st.sidebar.subheader("Delete a Task")
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
    st.sidebar.write("No tasks available to update or delete.")

# Move Reset Database Option to the End of Sidebar
st.sidebar.markdown("---")
if st.sidebar.button("Reset Database (End)"):
    reset_database()
    st.success("Database has been reset!")
    st.session_state.refresh = not st.session_state.get("refresh", False)
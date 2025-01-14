import streamlit as st
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

# Initialize refresh state
if "refresh_tasks" not in st.session_state:
    st.session_state.refresh_tasks = True

# Fetch tasks dynamically when needed
if st.session_state.refresh_tasks:
    tasks = get_tasks()  # Fetch from the database
    st.session_state.refresh_tasks = False  # Reset flag

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
    st.session_state.refresh_tasks = True  # Trigger refresh

# Main Page: Tasks Grouped by Status
if tasks:
    # Map urgency and importance to specific scale labels
    for task in tasks:
        task["Urgency Label"] = map_scale(task["urgency"])
        task["Importance Label"] = map_scale(task["importance"])

    # Task categories
    task_status_mapping = {
        "To Do": [task for task in tasks if task["status"] == "to do"],
        "Doing": [task for task in tasks if task["status"] == "doing"],
        "Done": [task for task in tasks if task["status"] == "done"],
    }

    # Display tasks by category
    for status, data in task_status_mapping.items():
        st.subheader(status)
        if data:
            st.dataframe(
                [{"Task ID": task["id"],
                  "Title": task["title"],
                  "Description": task["description"],
                  "Urgency": task["Urgency Label"],
                  "Importance": task["Importance Label"],
                  "Created At": task["created_at"],
                  "Updated At": task["updated_at"]} for task in data],
                use_container_width=True,
            )
        else:
            st.write(f"No {status.lower()} tasks.")
else:
    st.write("No tasks found.")

# Sidebar: Update Existing Task
st.sidebar.markdown("---")
st.sidebar.subheader("Update Existing Task")

if tasks:
    with st.sidebar.form("update_task_form"):
        # Dropdown to select the task to update
        task_id = st.selectbox(
            "Select Task ID to Update",
            [task["id"] for task in tasks],
            format_func=lambda x: f"Task {x}: {next(task['title'] for task in tasks if task['id'] == x)}",
        )

        # Fetch current values for the selected task
        selected_task = next(task for task in tasks if task["id"] == task_id)

        # Allow transitioning based on current status
        current_status = selected_task["status"]
        if current_status == "to do":
            status_options = ["doing", "done"]
        elif current_status == "doing":
            status_options = ["to do", "done"]
        elif current_status == "done":
            status_options = ["doing"]

        status = st.radio(
            "Status",
            options=status_options,
            index=status_options.index(current_status) if current_status in status_options else 0,
            horizontal=True,
        )

        # Allow updating other task details
        title = st.text_input("Title", value=selected_task["title"])
        description = st.text_area("Description", value=selected_task["description"])
        urgency = st.slider("Urgency", 1, 5, selected_task["urgency"])
        importance = st.slider("Importance", 1, 5, selected_task["importance"])

        # Submit button
        update_submitted = st.form_submit_button("Update Task")

        if update_submitted:
            # Update the task in the database
            update_task_status(task_id, status)  # Update the status
            update_task_details(
                task_id, title, description, urgency, importance
            )  # Update other details
            st.success(f"Task {task_id} updated successfully!")
            st.session_state.refresh_tasks = True  # Trigger refresh
else:
    st.sidebar.write("No tasks available to update.")

# Sidebar: Delete Task
st.sidebar.markdown("---")
st.sidebar.subheader("Delete a Task")
if tasks:
    task_id_to_delete = st.sidebar.selectbox(
        "Select Task ID to Delete",
        [task["id"] for task in tasks],
        format_func=lambda x: f"Task {x}: {next(task['title'] for task in tasks if task['id'] == x)}",
    )
    if st.sidebar.button("Delete Task"):
        delete_task(task_id_to_delete)
        st.success(f"Task {task_id_to_delete} deleted successfully!")
        st.session_state.refresh_tasks = True  # Trigger refresh
else:
    st.sidebar.write("No tasks available to delete.")

# Move Reset Database Option to the End of Sidebar
st.sidebar.markdown("---")
if st.sidebar.button("Reset Database (End)"):
    reset_database()
    st.success("Database has been reset!")
    st.session_state.refresh_tasks = True  # Trigger refresh
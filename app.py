import streamlit as st
from utils.database import (
    initialize_db,
    add_task,
    get_tasks,
    update_task_status,
    update_task_details,
    delete_task,
    reset_database,
)

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
    # Title input
    st.text_input(
        "Task Title", 
        placeholder="Enter your task title", 
        key="title", 
        label_visibility="collapsed"
    )
    # Sliders
    st.slider("Urgency", 1, 5, 3, key="urgency")
    st.slider("Importance", 1, 5, 3, key="importance")

    submitted = st.form_submit_button("Add Task")
    if submitted and st.session_state.title:
        add_task(
            st.session_state.title,
            st.session_state.urgency,
            st.session_state.importance,
        )
        st.success("Task added successfully!")
        st.rerun()

# Main Page: Tasks Grouped by Status
tasks = get_tasks()
if tasks:
    # Map urgency and importance to specific scale labels and calculate Eisenhower ratio
    for task in tasks:
        task["Urgency Label"] = map_scale(task["urgency"])
        task["Importance Label"] = map_scale(task["importance"])
        task["Eisenhower Ratio"] = task["importance"] * task["urgency"]

    # Task categories
    task_status_mapping = {
        "To Do": [t for t in tasks if t["status"] == "to do"],
        "Doing": [t for t in tasks if t["status"] == "doing"],
        "Done": [t for t in tasks if t["status"] == "done"],
    }

    # Display tasks by category
    for status, data in task_status_mapping.items():
        st.subheader(status)
        if data:
            st.dataframe(
                [
                    {
                        "Task ID": t["id"],
                        "Title": t["title"],
                        "Urgency": t["Urgency Label"],
                        "Importance": t["Importance Label"],
                        "Eisenhower Ratio": t["Eisenhower Ratio"],
                        "Created At": t["created_at"],
                        "Updated At": t["updated_at"],
                    }
                    for t in sorted(data, key=lambda x: x["Eisenhower Ratio"], reverse=True)
                ],
                use_container_width=True,
            )
        else:
            st.write(f"No {status.lower()} tasks.")
else:
    st.write("No tasks found.")

# Sidebar: Update Existing Task
st.sidebar.subheader('', divider='rainbow')
st.sidebar.subheader("Update Existing Task")

if tasks:
    with st.sidebar.form("update_task_form"):
        task_id = st.selectbox(
            "Select Task ID to Update",
            [t["id"] for t in tasks],
            format_func=lambda x: f"Task {x}: {next(t['title'] for t in tasks if t['id'] == x)}",
        )
        selected_task = next(t for t in tasks if t["id"] == task_id)

        # Static options for status
        status_options = ["to do", "doing", "done"]
        status = st.radio(
            "Status",
            options=status_options,
            index=status_options.index(selected_task["status"]),
            horizontal=True,
        )

        # Title + sliders
        title = st.text_input("Title", value=selected_task["title"])
        urgency = st.slider("Urgency", 1, 5, selected_task["urgency"])
        importance = st.slider("Importance", 1, 5, selected_task["importance"])

        update_submitted = st.form_submit_button("Update Task")

        if update_submitted:
            # Update the task in the database
            update_task_status(task_id, status)
            update_task_details(task_id, title, urgency, importance)
            st.success(f"Task {task_id} updated successfully!")
            st.rerun()
else:
    st.sidebar.write("No tasks available to update.")

# Sidebar: Delete Task
st.sidebar.subheader('', divider='rainbow')
st.sidebar.subheader("Delete a Task")
if tasks:
    task_id_to_delete = st.sidebar.selectbox(
        "Select Task ID to Delete",
        [t["id"] for t in tasks],
        format_func=lambda x: f"Task {x}: {next(t['title'] for t in tasks if t['id'] == x)}",
    )
    if st.sidebar.button("Delete Task"):
        delete_task(task_id_to_delete)
        st.sidebar.success(f"Task {task_id_to_delete} deleted successfully!")
        st.rerun()
else:
    st.sidebar.write("No tasks available to delete.")

# Sidebar: Reset Database
st.sidebar.subheader('', divider='rainbow')
if st.sidebar.button("Reset Database (End)"):
    reset_database()
    st.sidebar.success("Database has been reset!")
    st.rerun()
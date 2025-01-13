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

# Right Column: Task List
with col2:
    st.header("Task List")
    tasks = get_tasks()
    if tasks:
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

        # Display tasks in a table with interactive buttons for status change
        for idx, row in df_tasks.iterrows():
            st.write(f"**Task ID:** {row['Task ID']}")
            st.write(f"**Title:** {row['Title']}")
            st.write(f"**Description:** {row['Description']}")
            st.write(f"**Urgency:** {row['Urgency']} | **Importance:** {row['Importance']}")
            st.write(f"**Created At:** {row['Created At']}")
            current_status = row["Status"]
            new_status = st.selectbox(
                f"Change Status for Task {row['Task ID']}",
                options=["created", "done"],
                index=0 if current_status == "created" else 1,
                key=f"status_{row['Task ID']}",
            )
            if new_status != current_status:
                if st.button(f"Update Task {row['Task ID']}"):
                    update_task_status(row["Task ID"], new_status)
                    st.success(f"Task '{row['Title']}' updated to '{new_status}'!")
                    st.experimental_rerun()
            st.divider()
    else:
        st.write("No tasks found.")

# Metrics Section
st.header("Metrics")
metrics = calculate_metrics()
st.write(f"Tasks completed today: {metrics['completed_today']}")
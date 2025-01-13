import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
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
col1, col2 = st.columns([1.5, 2])  # Adjusted column width ratio for better balance

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

# Right Column: Task DataFrame and Metrics
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

        # Configure AgGrid for interactive editing
        gb = GridOptionsBuilder.from_dataframe(df_tasks)
        gb.configure_default_column(editable=True)
        gb.configure_column("Status", editable=True, cellEditor="agSelectCellEditor", cellEditorParams={"values": ["created", "done"]})
        grid_options = gb.build()

        # Display editable DataFrame
        grid_response = AgGrid(
            df_tasks,
            gridOptions=grid_options,
            update_mode="MODEL_CHANGED",
            editable=True,
            height=800,
            fit_columns_on_grid_load=True,
        )

        # Check for changes in the DataFrame
        updated_df = grid_response["data"]

        # Apply changes to the database
        for _, row in updated_df.iterrows():
            if row["Status"] != df_tasks.loc[row.name, "Status"]:  # Check if the status has changed
                update_task_status(row["Task ID"], row["Status"])
                st.success(f"Task '{row['Title']}' updated to '{row['Status']}'!")
    else:
        st.write("No tasks found.")

    # Metrics Section
    st.header("Metrics")
    metrics = calculate_metrics()
    st.write(f"Tasks completed today: {metrics['completed_today']}")
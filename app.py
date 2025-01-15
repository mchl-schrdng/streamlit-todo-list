import streamlit as st
from utils.database import initialize_db, get_tasks
from components.sidebar import render_sidebar
from components.task_display import display_tasks
from components.analytics import display_analytics

# Initialize the database
initialize_db()

# Set up the app layout
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
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", options=["Task Manager", "Analytics"])
st.divider()
render_sidebar()

# Main Content
if menu == "Task Manager":
    tasks = get_tasks()
    display_tasks(tasks)
elif menu == "Analytics":
    tasks = get_tasks()
    display_analytics(tasks)
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

# Sidebar Navigation
render_sidebar()
menu = st.sidebar.radio("Navigation", options=["Task Manager", "Analytics"])

# Main Content
if menu == "Task Manager":
    tasks = get_tasks()
    display_tasks(tasks)
elif menu == "Analytics":
    tasks = get_tasks()
    display_analytics(tasks)
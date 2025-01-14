import streamlit as st
from utils.database import initialize_db, get_tasks
from components.sidebar import render_sidebar
from components.task_display import display_tasks

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
load_css("static/styles.css")

# Render Sidebar
render_sidebar()

# Main Content: Display Tasks
tasks = get_tasks()
display_tasks(tasks)
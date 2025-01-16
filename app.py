import streamlit as st
from utils.database import initialize_db, get_tasks
from utils.theme_manager import apply_theme
from components.sidebar import render_sidebar
from components.task_display import display_tasks
from components.analytics import display_analytics

# Initialize the database
initialize_db()

# Configure the page
st.set_page_config(
    page_title="Todooolist",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🤖"
)

# Apply the theme
apply_theme()

# Initialize session state menu
if "menu" not in st.session_state:
    st.session_state.menu = "Task Manager"

# Sidebar navigation
st.sidebar.write("### Navigation")
col1, col2 = st.sidebar.columns(2)

if col1.button("Task Manager"):
    st.session_state.menu = "Task Manager"
if col2.button("Analytics"):
    st.session_state.menu = "Analytics"

# Display content based on the selected menu
if st.session_state.menu == "Task Manager":
    tasks = get_tasks()
    display_tasks(tasks)
elif st.session_state.menu == "Analytics":
    tasks = get_tasks()
    display_analytics(tasks)

# Render additional sidebar components
st.sidebar.markdown("---")
render_sidebar()
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

# Load CSS from the static/styles.css file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply global styling
load_css("static/styles.css")

# Render Sidebar
render_sidebar()

# Main Content: Display Tasks
tasks = get_tasks()
display_tasks(tasks)
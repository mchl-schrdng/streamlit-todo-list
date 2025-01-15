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

# Initialize a default page in session state if not set
if "menu" not in st.session_state:
    st.session_state.menu = "Task Manager"

st.sidebar.write("### Navigation")
col1, col2 = st.sidebar.columns(2)

# Two separate buttons to switch pages
if col1.button("Task Manager"):
    st.session_state.menu = "Task Manager"
if col2.button("Analytics"):
    st.session_state.menu = "Analytics"

# Main Content based on current 'menu' in session state
if st.session_state.menu == "Task Manager":
    tasks = get_tasks()
    display_tasks(tasks)
elif st.session_state.menu == "Analytics":
    tasks = get_tasks()
    display_analytics(tasks)

st.sidebar.markdown("---")
# Render the sidebar for other actions (add/update/delete tasks)
render_sidebar()
import random
import streamlit as st
from utils.database import initialize_db, get_tasks
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

gradients = [
 #   "linear-gradient(to right, #6a11cb, #2575fc)",
 #   "linear-gradient(to right, #ff7e5f, #feb47b)",
    "linear-gradient(to right, #00c6ff, #0072ff)",
 #   "linear-gradient(to right, #6441a5, #2a0845)",
]

selected_gradient = random.choice(gradients)

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: {selected_gradient};
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

if "menu" not in st.session_state:
    st.session_state.menu = "Task Manager"

st.sidebar.write("### Navigation")
col1, col2 = st.sidebar.columns(2)

if col1.button("Task Manager"):
    st.session_state.menu = "Task Manager"
if col2.button("Analytics"):
    st.session_state.menu = "Analytics"

if st.session_state.menu == "Task Manager":
    tasks = get_tasks()
    display_tasks(tasks)
elif st.session_state.menu == "Analytics":
    tasks = get_tasks()
    display_analytics(tasks)

st.sidebar.markdown("---")
render_sidebar()
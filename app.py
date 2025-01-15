import streamlit as st
from utils.database import initialize_db, get_tasks
from components.sidebar import render_sidebar
from components.task_display import display_tasks
from components.analytics import display_analytics

initialize_db()

st.set_page_config(
    page_title="Todooolist",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🤖"
)

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
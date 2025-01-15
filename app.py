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

gradients = [
    "linear-gradient(to right, #6a11cb, #2575fc)",
    "linear-gradient(to right, #ff7e5f, #feb47b)",
    "linear-gradient(to right, #00c6ff, #0072ff)",
    "linear-gradient(to right, #43cea2, #185a9d)",
    "linear-gradient(to right, #6441a5, #2a0845)",
]

selected_gradients = random.sample(gradients, 10)

for gradient in selected_gradients:
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: {gradient};
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.write(f"Using Gradient: {gradient}")

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
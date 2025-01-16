import streamlit as st

def apply_theme():
    # Define gradients for light and dark modes
    gradients = {
        "Light Mode": "linear-gradient(to right, #ff7e5f, #feb47b)",
        "Dark Mode": "linear-gradient(to right, #6441a5, #2a0845)"
    }

    # Add a switch for dark/light mode in the sidebar
    st.sidebar.write("### Appearance")
    is_dark_mode = st.sidebar.toggle("Dark Mode", value=False)

    # Set the selected gradient based on the switch state
    selected_gradient = gradients["Dark Mode"] if is_dark_mode else gradients["Light Mode"]

    # Apply the selected gradient as the background
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
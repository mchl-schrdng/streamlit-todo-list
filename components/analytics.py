import streamlit as st
import plotly.express as px
from utils.plotly_utils import apply_transparent_layout
from datetime import datetime

def display_analytics(tasks):
    """Displays a time series chart of the number of tasks created over time."""
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # Time Series: Number of Tasks Created Over Time
    st.subheader("Tasks Created Over Time")
    time_series_data = {}
    for task in tasks:
        # Parse the created_at date and group by day
        created_date = datetime.strptime(task["created_at"], "%Y-%m-%d %H:%M:%S").date()
        time_series_data[created_date] = time_series_data.get(created_date, 0) + 1

    # Convert the time series data to a sorted list
    sorted_time_series = sorted(time_series_data.items())
    dates, counts = zip(*sorted_time_series)

    # Create the time series chart
    time_series_chart = px.line(
        x=dates,
        y=counts,
        labels={"x": "Date", "y": "Number of Tasks"},
        title="Number of Tasks Created Over Time",
    )
    time_series_chart = apply_transparent_layout(time_series_chart)
    st.plotly_chart(time_series_chart, use_container_width=True)
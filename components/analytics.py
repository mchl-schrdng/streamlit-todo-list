import streamlit as st
import plotly.express as px
from utils.plotly_utils import apply_transparent_layout
from datetime import datetime

def display_analytics(tasks):
    """Displays analytics using Plotly with a transparent background."""
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # Pie Chart: Task Distribution by Status
    st.subheader("Task Distribution by Status")
    task_status_counts = {task["status"]: 0 for task in tasks}
    for task in tasks:
        task_status_counts[task["status"]] += 1

    pie_chart = px.pie(
        names=list(task_status_counts.keys()),
        values=list(task_status_counts.values()),
        title="Tasks by Status",
        hole=0.4,  # Donut chart
    )
    pie_chart = apply_transparent_layout(pie_chart)
    st.plotly_chart(pie_chart, use_container_width=True)

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
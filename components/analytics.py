import streamlit as st
import plotly.express as px
from utils.plotly_utils import apply_transparent_layout
from datetime import datetime

def display_analytics(tasks):
    """Displays top 4 visualizations in a two-column layout."""
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # Prepare Data
    task_status_counts = {task["status"]: 0 for task in tasks}
    time_series_data = {}
    urgency_counts = {task["urgency"]: 0 for task in tasks}
    scatter_data = []

    for task in tasks:
        # Status counts
        task_status_counts[task["status"]] += 1

        # Time series
        created_date = datetime.strptime(task["created_at"], "%Y-%m-%d %H:%M:%S").date()
        time_series_data[created_date] = time_series_data.get(created_date, 0) + 1

        # Urgency counts
        urgency_counts[task["urgency"]] += 1

        # Scatter data
        scatter_data.append({
            "title": task["title"],
            "urgency": task["urgency"],
            "importance": task["importance"],
            "status": task["status"],
        })

    # Sort time series data
    sorted_time_series = sorted(time_series_data.items())
    dates, counts = zip(*sorted_time_series)

    # Create Visualizations
    # 1. Pie Chart: Task Distribution by Status
    pie_chart = px.pie(
        names=list(task_status_counts.keys()),
        values=list(task_status_counts.values()),
        title="Task Distribution by Status",
        hole=0.4,
    )
    pie_chart = apply_transparent_layout(pie_chart)

    # 2. Time Series: Tasks Created Over Time
    time_series_chart = px.line(
        x=dates,
        y=counts,
        labels={"x": "Date", "y": "Number of Tasks"},
        title="Tasks Created Over Time",
    )
    time_series_chart = apply_transparent_layout(time_series_chart)

    # 3. Scatter Plot: Urgency vs. Importance
    scatter_chart = px.scatter(
        scatter_data,
        x="urgency",
        y="importance",
        color="status",
        hover_data=["title"],
        title="Urgency vs. Importance",
    )
    scatter_chart = apply_transparent_layout(scatter_chart)

    # 4. Bar Chart: Task Count by Urgency Level
    bar_chart = px.bar(
        x=list(urgency_counts.keys()),
        y=list(urgency_counts.values()),
        labels={"x": "Urgency Level", "y": "Task Count"},
        title="Task Count by Urgency Level",
    )
    bar_chart = apply_transparent_layout(bar_chart)

    # Display Visualizations in Two Columns
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(pie_chart, use_container_width=True)
        st.plotly_chart(scatter_chart, use_container_width=True)

    with col2:
        st.plotly_chart(time_series_chart, use_container_width=True)
        st.plotly_chart(bar_chart, use_container_width=True)
import streamlit as st
import plotly.express as px
from utils.plotly_utils import apply_transparent_layout
from datetime import datetime
from collections import defaultdict

def display_analytics(tasks):
    """Displays top 4 visualizations in a two-column layout."""
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # Prepare Data
    task_status_counts = defaultdict(int)
    time_series_data = defaultdict(int)
    urgency_trends = defaultdict(list)
    importance_trends = defaultdict(list)
    status_over_time = defaultdict(lambda: defaultdict(int))

    for task in tasks:
        # Status counts
        task_status_counts[task["status"]] += 1

        # Time series
        created_date = datetime.strptime(task["created_at"], "%Y-%m-%d %H:%M:%S").date()
        time_series_data[created_date] += 1

        # Trends for urgency and importance
        urgency_trends[created_date].append(task["urgency"])
        importance_trends[created_date].append(task["importance"])

        # Status over time
        status_over_time[created_date][task["status"]] += 1

    # Calculate average urgency and importance over time
    urgency_avg = {date: sum(values) / len(values) for date, values in urgency_trends.items()}
    importance_avg = {date: sum(values) / len(values) for date, values in importance_trends.items()}

    # Sort data
    sorted_time_series = sorted(time_series_data.items())
    sorted_urgency = sorted(urgency_avg.items())
    sorted_importance = sorted(importance_avg.items())

    # Prepare data for status over time
    status_data = []
    for date, statuses in status_over_time.items():
        for status, count in statuses.items():
            status_data.append({"Date": date, "Status": status, "Count": count})

    # Prepare data for visualizations
    dates, task_counts = zip(*sorted_time_series)
    urgency_dates, urgency_values = zip(*sorted_urgency)
    importance_dates, importance_values = zip(*sorted_importance)

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
        y=task_counts,
        labels={"x": "Date", "y": "Number of Tasks"},
        title="Tasks Created Over Time",
    )
    time_series_chart = apply_transparent_layout(time_series_chart)

    # 3. Line Chart: Average Urgency and Importance Over Time
    trend_chart = px.line(
        x=urgency_dates + importance_dates,
        y=urgency_values + importance_values,
        color=["Urgency"] * len(urgency_dates) + ["Importance"] * len(importance_dates),
        labels={"x": "Date", "y": "Average Value", "color": "Metric"},
        title="Urgency and Importance Trends Over Time",
    )
    trend_chart = apply_transparent_layout(trend_chart)

    # 4. Bar Chart: Task Distribution by Status Over Time
    status_chart = px.bar(
        status_data,
        x="Date",
        y="Count",
        color="Status",
        barmode="stack",
        labels={"Date": "Date", "Count": "Task Count", "Status": "Task Status"},
        title="Task Distribution by Status Over Time",
    )
    status_chart = apply_transparent_layout(status_chart)

    # Display Visualizations in Two Columns
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(pie_chart, use_container_width=True)
        st.plotly_chart(trend_chart, use_container_width=True)

    with col2:
        st.plotly_chart(time_series_chart, use_container_width=True)
        st.plotly_chart(status_chart, use_container_width=True)
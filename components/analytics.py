import streamlit as st
import plotly.express as px
from datetime import datetime
from collections import defaultdict
from utils.plotly_utils import apply_transparent_layout

def display_analytics(tasks):
    """
    Displays four basic analytics visualizations:
      1) Pie Chart: Task Distribution by Status
      2) Line Chart: Tasks Created Over Time
      3) Line Chart: Average Urgency and Importance Over Time
      4) Stacked Bar Chart: Task Distribution by Status Over Time

    Assumes 'created_at' is stored as 'YYYY-MM-DD' (date only).
    """

    # If no tasks are found, just show a message
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # Prepare data structures
    task_status_counts = defaultdict(int)
    time_series_data = defaultdict(int)
    urgency_trends = defaultdict(list)
    importance_trends = defaultdict(list)
    status_over_time = defaultdict(lambda: defaultdict(int))

    # Parse each task
    for task in tasks:
        # Convert 'created_at' from "YYYY-MM-DD" to a Python date
        created_date = datetime.strptime(task["created_at"], "%Y-%m-%d").date()

        # Status distribution
        task_status_counts[task["status"]] += 1

        # Tasks Created Over Time
        time_series_data[created_date] += 1

        # Urgency & Importance Trends
        urgency_trends[created_date].append(task["urgency"])
        importance_trends[created_date].append(task["importance"])

        # Status Over Time (for stacked bar)
        status_over_time[created_date][task["status"]] += 1

    # Compute averages for urgency and importance per date
    urgency_avg = {
        date: sum(values) / len(values)
        for date, values in urgency_trends.items()
    }
    importance_avg = {
        date: sum(values) / len(values)
        for date, values in importance_trends.items()
    }

    # Sort the dictionary items for time-based plots
    sorted_time_series = sorted(time_series_data.items())   # e.g. [(date, count), ...]
    sorted_urgency = sorted(urgency_avg.items())            # e.g. [(date, avg_urg), ...]
    sorted_importance = sorted(importance_avg.items())      # e.g. [(date, avg_imp), ...]

    # Flatten status_over_time for stacked bar
    status_data = []
    for date, statuses in status_over_time.items():
        for s, count in statuses.items():
            status_data.append({
                "Date": date,
                "Status": s,
                "Count": count
            })

    # Unpack for time-series charts
    if sorted_time_series:
        dates, task_counts = zip(*sorted_time_series)
    else:
        dates, task_counts = [], []

    if sorted_urgency:
        urgency_dates, urgency_values = zip(*sorted_urgency)
    else:
        urgency_dates, urgency_values = [], []

    if sorted_importance:
        importance_dates, importance_values = zip(*sorted_importance)
    else:
        importance_dates, importance_values = [], []

    # -------------------------------------------------------------------------
    # 1) Pie Chart: Task Distribution by Status
    # -------------------------------------------------------------------------
    pie_chart = px.pie(
        names=list(task_status_counts.keys()),
        values=list(task_status_counts.values()),
        title="Task Distribution by Status",
        hole=0.4,
    )
    pie_chart = apply_transparent_layout(pie_chart)

    # -------------------------------------------------------------------------
    # 2) Time Series: Tasks Created Over Time
    # -------------------------------------------------------------------------
    time_series_chart = px.line(
        x=dates,
        y=task_counts,
        labels={"x": "Date", "y": "Number of Tasks"},
        title="Tasks Created Over Time",
    )
    time_series_chart = apply_transparent_layout(time_series_chart)
    # Force date format to show only the date
    time_series_chart.update_xaxes(tickformat="%b %d, %Y")

    # -------------------------------------------------------------------------
    # 3) Line Chart: Average Urgency and Importance Over Time
    # -------------------------------------------------------------------------
    combined_x = list(urgency_dates) + list(importance_dates)
    combined_y = list(urgency_values) + list(importance_values)
    combined_color = (["Urgency"] * len(urgency_dates)
                      + ["Importance"] * len(importance_dates))

    trend_chart = px.line(
        x=combined_x,
        y=combined_y,
        color=combined_color,
        labels={"x": "Date", "y": "Average Value", "color": "Metric"},
        title="Urgency and Importance Trends Over Time",
    )
    trend_chart = apply_transparent_layout(trend_chart)
    trend_chart.update_xaxes(tickformat="%b %d, %Y")

    # -------------------------------------------------------------------------
    # 4) Stacked Bar: Task Distribution by Status Over Time
    # -------------------------------------------------------------------------
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
    status_chart.update_xaxes(tickformat="%b %d, %Y")

    # -------------------------------------------------------------------------
    # Display the charts in a 2x2 layout
    # -------------------------------------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(pie_chart, use_container_width=True)
        st.plotly_chart(trend_chart, use_container_width=True)

    with col2:
        st.plotly_chart(time_series_chart, use_container_width=True)
        st.plotly_chart(status_chart, use_container_width=True)
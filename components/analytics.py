import streamlit as st
import plotly.express as px
from utils.plotly_utils import apply_transparent_layout

def display_analytics(tasks):
    """Displays analytics using Plotly with a transparent background."""
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # Display tasks in an interactive table
    st.subheader("Task Data Overview")
    st.dataframe(tasks, use_container_width=True)

    # Pie Chart: Task Distribution by Status
    st.subheader("Task Distribution by Status")
    task_status_counts = {task["status"]: 0 for task in tasks}
    for task in tasks:
        task_status_counts[task["status"]] += 1

    pie_chart = px.pie(
        names=list(task_status_counts.keys()),
        values=list(task_status_counts.values()),
        title="Tasks by Status",
        hole=0.4,
    )
    pie_chart = apply_transparent_layout(pie_chart)
    st.plotly_chart(pie_chart, use_container_width=True)

    # Scatter Plot: Urgency vs. Importance
    st.subheader("Urgency vs. Importance")
    scatter_data = [
        {
            "title": task["title"],
            "urgency": task["urgency"],
            "importance": task["importance"],
            "status": task["status"],
        }
        for task in tasks
    ]
    scatter_chart = px.scatter(
        scatter_data,
        x="urgency",
        y="importance",
        color="status",
        hover_data=["title"],
        title="Urgency vs. Importance by Status",
    )
    scatter_chart = apply_transparent_layout(scatter_chart)
    st.plotly_chart(scatter_chart, use_container_width=True)

    # Bar Chart: Task Count by Urgency Level
    st.subheader("Task Count by Urgency Level")
    urgency_counts = {task["urgency"]: 0 for task in tasks}
    for task in tasks:
        urgency_counts[task["urgency"]] += 1

    bar_chart = px.bar(
        x=list(urgency_counts.keys()),
        y=list(urgency_counts.values()),
        labels={"x": "Urgency Level", "y": "Task Count"},
        title="Task Count by Urgency Level",
    )
    bar_chart = apply_transparent_layout(bar_chart)
    st.plotly_chart(bar_chart, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from collections import defaultdict
from utils.plotly_utils import apply_transparent_layout

def display_analytics(tasks):
    """
    Displays the original 4 visualizations plus 4 additional ones for deeper insights.
    If you do not have 'completed_at' in your tasks data, remove or comment out 
    the 'display_completion_time_by_tag' function call.
    """

    st.header("Core Analytics")

    # -------------------------------
    # 1) Check if any tasks exist
    # -------------------------------
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    # -------------------------------------------------------------------------
    # 2) Prepare Data for Original Charts
    # -------------------------------------------------------------------------
    task_status_counts = defaultdict(int)        # For pie chart
    time_series_data = defaultdict(int)          # For tasks created over time
    urgency_trends = defaultdict(list)           # For average urgency over time
    importance_trends = defaultdict(list)        # For average importance over time
    status_over_time = defaultdict(lambda: defaultdict(int))  # For stacked bar / CFD

    for task in tasks:
        # Status counts
        task_status_counts[task["status"]] += 1

        # Time series (parse creation date)
        created_date = datetime.strptime(task["created_at"], "%Y-%m-%d %H:%M:%S").date()
        time_series_data[created_date] += 1

        # Trends for urgency and importance
        urgency_trends[created_date].append(task["urgency"])
        importance_trends[created_date].append(task["importance"])

        # Status over time
        status_over_time[created_date][task["status"]] += 1

    # Calculate average urgency and importance per date
    urgency_avg = {
        date: sum(values) / len(values) for date, values in urgency_trends.items()
    }
    importance_avg = {
        date: sum(values) / len(values) for date, values in importance_trends.items()
    }

    # Sort data for time-based charts
    sorted_time_series = sorted(time_series_data.items())  # e.g. [(date, count), ...]
    sorted_urgency = sorted(urgency_avg.items())
    sorted_importance = sorted(importance_avg.items())

    # Prepare data for status over time (stacked bar)
    status_data = []
    for date, statuses in status_over_time.items():
        for status, count in statuses.items():
            status_data.append({"Date": date, "Status": status, "Count": count})

    # Unpack for time series chart
    dates, task_counts = zip(*sorted_time_series) if sorted_time_series else ([], [])
    urgency_dates, urgency_values = zip(*sorted_urgency) if sorted_urgency else ([], [])
    importance_dates, importance_values = (
        zip(*sorted_importance) if sorted_importance else ([], [])
    )

    # -------------------------------------------------------------------------
    # 3) Original Charts
    # -------------------------------------------------------------------------

    # 3.1 Pie Chart: Task Distribution by Status
    pie_chart = px.pie(
        names=list(task_status_counts.keys()),
        values=list(task_status_counts.values()),
        title="Task Distribution by Status",
        hole=0.4,
    )
    pie_chart = apply_transparent_layout(pie_chart)

    # 3.2 Time Series: Tasks Created Over Time
    time_series_chart = px.line(
        x=dates,
        y=task_counts,
        labels={"x": "Date", "y": "Number of Tasks"},
        title="Tasks Created Over Time",
    )
    time_series_chart = apply_transparent_layout(time_series_chart)

    # 3.3 Line Chart: Average Urgency and Importance Over Time
    # Because both are on a 1–5 scale, we can plot them on the same axis
    combined_x = list(urgency_dates) + list(importance_dates)
    combined_y = list(urgency_values) + list(importance_values)
    combined_color = ["Urgency"] * len(urgency_dates) + ["Importance"] * len(importance_dates)

    trend_chart = px.line(
        x=combined_x,
        y=combined_y,
        color=combined_color,
        labels={"x": "Date", "y": "Average Value", "color": "Metric"},
        title="Urgency and Importance Trends Over Time",
    )
    trend_chart = apply_transparent_layout(trend_chart)

    # 3.4 Bar Chart: Task Distribution by Status Over Time (stacked)
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

    # Display the original 4 charts in a 2x2 layout
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(pie_chart, use_container_width=True)
        st.plotly_chart(trend_chart, use_container_width=True)
    with col2:
        st.plotly_chart(time_series_chart, use_container_width=True)
        st.plotly_chart(status_chart, use_container_width=True)

    # -------------------------------------------------------------------------
    # 4) Additional Visualizations (4 Proposed)
    # -------------------------------------------------------------------------
    st.header("Additional Analytics")

    # Convert tasks list to a DataFrame for convenience
    df_tasks = pd.DataFrame(tasks)

    # --------------------------
    # 4.1 Scatter: Urgency vs. Importance
    # --------------------------
    st.subheader("Scatter Plot: Urgency vs. Importance")

    if not df_tasks.empty:
        # Add an "Eisenhower Ratio" if not already present
        if "Eisenhower Ratio" not in df_tasks.columns:
            df_tasks["Eisenhower Ratio"] = df_tasks["urgency"] * df_tasks["importance"]

        scatter_fig = px.scatter(
            df_tasks,
            x="urgency",
            y="importance",
            color="status",
            size="Eisenhower Ratio",  
            hover_data=["id", "title", "tag", "Eisenhower Ratio"],
            title="Urgency vs. Importance (Colored by Status)",
            labels={"urgency": "Urgency", "importance": "Importance"},
        )
        scatter_fig = apply_transparent_layout(scatter_fig)
        st.plotly_chart(scatter_fig, use_container_width=True)
    else:
        st.write("No data for scatter plot.")

    # --------------------------
    # 4.2 Heatmap: Task Count (Status vs. Tag)
    # --------------------------
    st.subheader("Heatmap: Status vs. Tag")

    if not df_tasks.empty:
        # Group by status and tag
        heatmap_df = (
            df_tasks.groupby(["status", "tag"])
            .size()
            .reset_index(name="count")
            .pivot(index="status", columns="tag", values="count")
            .fillna(0)
        )

        heatmap_fig = px.imshow(
            heatmap_df,
            color_continuous_scale="Blues",
            labels=dict(color="Task Count"),
            title="Task Distribution Heatmap (Status vs. Tag)",
        )
        heatmap_fig = apply_transparent_layout(heatmap_fig)
        st.plotly_chart(heatmap_fig, use_container_width=True)
    else:
        st.write("No data for status-tag heatmap.")

    # --------------------------
    # 4.3 Cumulative Flow Diagram (CFD)
    # --------------------------
    st.subheader("Cumulative Flow Diagram")

    # Re-use status_over_time from above
    if status_data:
        # Sort by date for an area chart
        cfd_df = pd.DataFrame(status_data).sort_values(by="Date")

        cfd_fig = px.area(
            cfd_df,
            x="Date",
            y="Count",
            color="Status",
            title="Cumulative Flow Diagram (Tasks Over Time by Status)",
            labels={"Count": "Number of Tasks"},
        )
        cfd_fig = apply_transparent_layout(cfd_fig)
        st.plotly_chart(cfd_fig, use_container_width=True)
    else:
        st.write("No data for cumulative flow diagram.")

    # --------------------------
    # 4.4 Bar Chart: Average Completion Time by Tag
    # --------------------------
    st.subheader("Average Completion Time by Tag")

    # This requires a 'completed_at' column or logic to detect final status date
    # We'll assume there's a completed_at field in your tasks for demonstration.
    if "completed_at" in df_tasks.columns:
        # Filter only tasks with a completion time
        df_completed = df_tasks[
            (df_tasks["status"] == "done") & (df_tasks["completed_at"].notnull())
        ].copy()

        if not df_completed.empty:
            # Convert to datetime
            df_completed["created_dt"] = pd.to_datetime(df_completed["created_at"])
            df_completed["completed_dt"] = pd.to_datetime(df_completed["completed_at"])
            # Calculate total hours or days to completion
            df_completed["completion_time_hrs"] = (
                df_completed["completed_dt"] - df_completed["created_dt"]
            ).dt.total_seconds() / 3600.0

            # Group by tag and take the mean
            grouped = df_completed.groupby("tag", as_index=False)["completion_time_hrs"].mean()
            grouped.rename(columns={"completion_time_hrs": "avg_hrs"}, inplace=True)

            comp_fig = px.bar(
                grouped,
                x="tag",
                y="avg_hrs",
                title="Average Completion Time by Tag (Hours)",
                labels={"tag": "Tag", "avg_hrs": "Average Hours to Complete"},
            )
            comp_fig = apply_transparent_layout(comp_fig)
            st.plotly_chart(comp_fig, use_container_width=True)
        else:
            st.write("No completed tasks with valid 'completed_at' field.")
    else:
        st.write("`completed_at` field not found. Skipping completion-time analysis.")
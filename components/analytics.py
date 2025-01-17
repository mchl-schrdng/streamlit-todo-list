import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from collections import defaultdict
from utils.plotly_utils import apply_transparent_layout

def display_analytics(tasks):
    if not tasks:
        st.write("No tasks available for analytics.")
        return

    task_status_counts = defaultdict(int)
    time_series_data = defaultdict(int)
    urgency_trends = defaultdict(list)
    importance_trends = defaultdict(list)
    status_over_time = defaultdict(lambda: defaultdict(int))

    for task in tasks:
        # Convert created_at to a date object
        created_date = datetime.strptime(task["created_at"], "%Y-%m-%d").date()

        # Aggregate counts
        task_status_counts[task["status"]] += 1
        time_series_data[created_date] += 1
        urgency_trends[created_date].append(task["urgency"])
        importance_trends[created_date].append(task["importance"])
        status_over_time[created_date][task["status"]] += 1

    # Calculate averages
    urgency_avg = {
        date: sum(values) / len(values)
        for date, values in urgency_trends.items()
    }
    importance_avg = {
        date: sum(values) / len(values)
        for date, values in importance_trends.items()
    }

    # Sort the data by date
    sorted_time_series = sorted(time_series_data.items())  # (date, count)
    sorted_urgency = sorted(urgency_avg.items())          # (date, avg_urgency)
    sorted_importance = sorted(importance_avg.items())    # (date, avg_importance)

    # Build a list for status-over-time data
    status_data = []
    for date_, statuses in status_over_time.items():
        for s, count in statuses.items():
            status_data.append(
                {"Date": date_, "Status": s, "Count": count}
            )

    # ------------------------------------------------
    # 1) TASK DISTRIBUTION (PIE CHART)
    # ------------------------------------------------
    pie_chart = px.pie(
        names=list(task_status_counts.keys()),
        values=list(task_status_counts.values()),
        title="Task Distribution by Status",
        hole=0.4,
    )
    pie_chart = apply_transparent_layout(pie_chart)

    # ------------------------------------------------
    # 2) TASKS CREATED OVER TIME (LINE CHART)
    # ------------------------------------------------
    if sorted_time_series:
        df_time = pd.DataFrame(sorted_time_series, columns=["Date", "Count"])
        # Convert to datetime (so Plotly sees it as a real date axis)
        df_time["Date"] = pd.to_datetime(df_time["Date"])

        time_series_chart = px.line(
            df_time,
            x="Date",
            y="Count",
            labels={"Date": "Date", "Count": "Number of Tasks"},
            title="Tasks Created Over Time",
        )
        time_series_chart = apply_transparent_layout(time_series_chart)
        time_series_chart.update_xaxes(type="date", tickformat="%b %d, %Y")
    else:
        time_series_chart = None

    # ------------------------------------------------
    # 3) URGENCY & IMPORTANCE (LINE CHART)
    # ------------------------------------------------
    if sorted_urgency or sorted_importance:
        # Build combined lists to plot on the same figure
        urgency_df = pd.DataFrame(sorted_urgency, columns=["Date", "MetricValue"])
        urgency_df["Metric"] = "Urgency"
        importance_df = pd.DataFrame(sorted_importance, columns=["Date", "MetricValue"])
        importance_df["Metric"] = "Importance"

        combined_df = pd.concat([urgency_df, importance_df], ignore_index=True)
        combined_df["Date"] = pd.to_datetime(combined_df["Date"])

        trend_chart = px.line(
            combined_df,
            x="Date",
            y="MetricValue",
            color="Metric",
            labels={
                "Date": "Date",
                "MetricValue": "Average Value",
                "Metric": "Metric",
            },
            title="Urgency and Importance Trends Over Time",
        )
        trend_chart = apply_transparent_layout(trend_chart)
        trend_chart.update_xaxes(type="date", tickformat="%b %d, %Y")
    else:
        trend_chart = None

    # ------------------------------------------------
    # 4) TASK STATUS OVER TIME (STACKED BAR)
    # ------------------------------------------------
    if status_data:
        df_status = pd.DataFrame(status_data)
        df_status["Date"] = pd.to_datetime(df_status["Date"])

        status_chart = px.bar(
            df_status,
            x="Date",
            y="Count",
            color="Status",
            barmode="stack",
            labels={
                "Date": "Date",
                "Count": "Task Count",
                "Status": "Task Status",
            },
            title="Task Distribution by Status Over Time",
        )
        status_chart = apply_transparent_layout(status_chart)
        status_chart.update_xaxes(type="date", tickformat="%b %d, %Y")
    else:
        status_chart = None

    # ------------------------------------------------
    # LAYOUT: TWO COLUMNS
    # ------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
        if trend_chart:
            st.plotly_chart(trend_chart, use_container_width=True)

    with col2:
        if time_series_chart:
            st.plotly_chart(time_series_chart, use_container_width=True)
        if status_chart:
            st.plotly_chart(status_chart, use_container_width=True)
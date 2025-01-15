import streamlit as st

def map_scale(value):
    """Maps scale value to descriptive label."""
    return {
        1: "Very Low",
        2: "Low",
        3: "Moderate",
        4: "High",
        5: "Very High",
    }.get(value, "Unknown")

def display_tasks(tasks):
    """Displays tasks grouped by status."""
    if not tasks:
        st.write("No tasks found.")
        return

    # Add labels and calculate Eisenhower ratio
    for task in tasks:
        task["Urgency Label"] = map_scale(task["urgency"])
        task["Importance Label"] = map_scale(task["importance"])
        task["Eisenhower Ratio"] = task["importance"] * task["urgency"]

    # Group tasks by status
    task_status_mapping = {
        "To Do": [t for t in tasks if t["status"] == "to do"],
        "Doing": [t for t in tasks if t["status"] == "doing"],
        "Done": [t for t in tasks if t["status"] == "done"],
    }

    # Display tasks for each status
    for status, data in task_status_mapping.items():
        st.subheader(status)
        if data:
            st.dataframe(
                [
                    {
                        "Task ID": t["id"],
                        "Title": t["title"],
                        "Tag": t["tag"] if t.get("tag") else "",  # <-- Display tag
                        "Urgency": t["Urgency Label"],
                        "Importance": t["Importance Label"],
                        "Eisenhower Ratio": t["Eisenhower Ratio"],
                        "Created At": t["created_at"],
                        "Updated At": t["updated_at"],
                    }
                    for t in sorted(data, key=lambda x: x["Eisenhower Ratio"], reverse=True)
                ],
                use_container_width=True,
            )
        else:
            st.write(f"No {status.lower()} tasks.")
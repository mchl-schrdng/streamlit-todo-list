import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime

def get_bq_client():
    """Create a BigQuery client from the TOML secrets."""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return bigquery.Client(
        credentials=credentials,
        # The project will match whatever you stored in secrets["bigquery"]["project_id"].
        project=st.secrets["bigquery"]["project_id"]
    )


def initialize_db():
    """
    Creates the tasks table in BigQuery if it doesn't already exist (DDL).
    """
    client = get_bq_client()
    dataset_id = st.secrets["bigquery"]["dataset_id"]
    table_id = st.secrets["bigquery"]["table_id"]
    table_full_name = f"`{client.project}.{dataset_id}.{table_id}`"

    create_ddl = f"""
    CREATE TABLE IF NOT EXISTS {table_full_name} (
      id INT64,
      title STRING NOT NULL,
      tag STRING,
      urgency INT64,
      importance INT64,
      status STRING,
      created_at DATE,
      updated_at DATE
    )
    """
    client.query(create_ddl).result()


def _get_table_full_name(client):
    """Helper to return the fully qualified table name: `project.dataset.table`."""
    dataset_id = st.secrets["bigquery"]["dataset_id"]
    table_id = st.secrets["bigquery"]["table_id"]
    return f"`{client.project}.{dataset_id}.{table_id}`"


def _get_max_id(client, table_full_name):
    """
    Helper to get the highest `id` from the table, so we can manually
    increment it (simulating AUTOINCREMENT).
    """
    query = f"SELECT IFNULL(MAX(id), 0) AS max_id FROM {table_full_name}"
    rows = client.query(query).result()
    row = list(rows)[0]
    return row.max_id or 0


def add_task(title, tag, urgency, importance):
    client = get_bq_client()
    table_full_name = _get_table_full_name(client)
    max_id = _get_max_id(client, table_full_name)
    new_id = max_id + 1

    query = f"""
        INSERT INTO {table_full_name} 
        (id, title, tag, urgency, importance, status, created_at, updated_at)
        VALUES (@id, @title, @tag, @urgency, @importance, 'to do', CURRENT_DATE(), CURRENT_DATE())
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id", "INT64", new_id),
            bigquery.ScalarQueryParameter("title", "STRING", title),
            bigquery.ScalarQueryParameter("tag", "STRING", tag),
            bigquery.ScalarQueryParameter("urgency", "INT64", urgency),
            bigquery.ScalarQueryParameter("importance", "INT64", importance),
        ]
    )
    client.query(query, job_config=job_config).result()


def get_tasks():
    client = get_bq_client()
    table_full_name = _get_table_full_name(client)
    query = f"""
        SELECT
          id, title, tag, urgency, importance, status,
          CAST(created_at AS STRING) AS created_at,
          CAST(updated_at AS STRING) AS updated_at
        FROM {table_full_name}
        ORDER BY id
    """
    rows = client.query(query).result()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row.id,
            "title": row.title,
            "tag": row.tag,
            "urgency": row.urgency,
            "importance": row.importance,
            "status": row.status,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        })
    return tasks


def update_task_status(task_id, status):
    client = get_bq_client()
    table_full_name = _get_table_full_name(client)
    query = f"""
        UPDATE {table_full_name}
        SET 
          status = @status,
          updated_at = CURRENT_DATE()
        WHERE id = @id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("status", "STRING", status),
            bigquery.ScalarQueryParameter("id", "INT64", task_id),
        ]
    )
    client.query(query, job_config=job_config).result()


def update_task_details(task_id, title, tag, urgency, importance):
    client = get_bq_client()
    table_full_name = _get_table_full_name(client)
    query = f"""
        UPDATE {table_full_name}
        SET
          title = @title,
          tag = @tag,
          urgency = @urgency,
          importance = @importance,
          updated_at = CURRENT_DATE()
        WHERE id = @id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("title", "STRING", title),
            bigquery.ScalarQueryParameter("tag", "STRING", tag),
            bigquery.ScalarQueryParameter("urgency", "INT64", urgency),
            bigquery.ScalarQueryParameter("importance", "INT64", importance),
            bigquery.ScalarQueryParameter("id", "INT64", task_id),
        ]
    )
    client.query(query, job_config=job_config).result()


def delete_task(task_id):
    client = get_bq_client()
    table_full_name = _get_table_full_name(client)
    query = f"""
        DELETE FROM {table_full_name}
        WHERE id = @id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id", "INT64", task_id),
        ]
    )
    client.query(query, job_config=job_config).result()


def reset_database():
    """
    Drops the tasks table and recreates it.
    """
    client = get_bq_client()
    table_full_name = _get_table_full_name(client)

    drop_ddl = f"DROP TABLE IF EXISTS {table_full_name}"
    client.query(drop_ddl).result()

    initialize_db()
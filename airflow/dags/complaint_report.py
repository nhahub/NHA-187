from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
import pandas as pd
from datetime import datetime, timedelta
import os

# Settings
REPORT_PATH = "/tmp/daily_complaints_report.xlsx"
EMAIL_TO = ["manager@company.com"] # Change this

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_and_generate_report():
    # 1. Connect to MySQL (Service name 'mysql' in docker-compose)
    # You must configure this connection in Airflow UI later, or pass credentials here
    hook = MySqlHook(mysql_conn_id='my_mysql_conn')
    
    # 2. Query Data (e.g., Get data from last 24 hours)
    sql = """
        SELECT * FROM complaints_analyzed 
        WHERE submitted_at >= NOW() - INTERVAL 1 DAY
    """
    df = hook.get_pandas_df(sql)
    
    if df.empty:
        print("No new complaints found.")
        # Create an empty file just so the email task doesn't fail
        df.to_excel(REPORT_PATH, index=False)
        return "no_data"

    # 3. Save to Excel
    print(f"Generating report with {len(df)} rows...")
    df.to_excel(REPORT_PATH, index=False)
    return "data_generated"

with DAG(
    'daily_smart_complaint_report',
    default_args=default_args,
    description='Extracts complaints from MySQL and emails report',
    schedule_interval='@weekly', # Runs once a week
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Generate Excel
    generate_report_task = PythonOperator(
        task_id='generate_excel_report',
        python_callable=extract_and_generate_report
    )

    # Task 2: Send Email
    send_email_task = EmailOperator(
        task_id='send_email_with_report',
        to=EMAIL_TO,
        subject='Daily Smart Complaint Report',
        html_content='<h3>Here is the daily summary of processed complaints.</h3>',
        files=[REPORT_PATH],
    )

    generate_report_task >> send_email_task
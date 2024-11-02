import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
from pinot_table_operator import PinotTableSubmitOperator
start_date = datetime(2024, 1, 11)
default_args = {
    'owner': "minhtranquang",
    "depends_on_past": False,
    "backfill": False,
    'start_date': start_date
}

with DAG('table_dag',
         default_args=default_args,
         description='A DAG to submit all table in a folder to Apache Pinot',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['table']
) as dag:
    
    start = EmptyOperator(
        task_id = 'start_task'
    )

    submit_tables = PinotTableSubmitOperator(
        task_id = 'submit_tables',
        folder_path = '/opt/airflow/dags/tables',
        pinot_url = 'http://pinot-controller:9000/tables'
    )

    end = EmptyOperator(
        task_id = 'end_task'
    )

    start >> submit_tables >> end
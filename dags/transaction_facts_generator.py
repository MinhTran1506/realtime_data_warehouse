from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from kafka_operator import KafkaProducerOperator

start_date = datetime(2024, 1, 11)
default_args = {
    'owner': "minhtranquang",
    "depends_on_past": False,
    "backfill": False,
    "start_date": start_date
}

with DAG(
    dag_id = 'transaction_facts_generator',
    default_args = default_args,
    description = "Transaction fact data generator into kafka",
    schedule_interval=timedelta(days=1),
    tags = ['fact_data'],
) as dag:
    start = EmptyOperator(
        task_id='start_task'
    )
    generate_txn_data = KafkaProducerOperator(
        task_id='generate_txn_fact_data',
        kafka_broker='kafka_broker:9092',
        kafka_topic='transaction_facts',
        num_records=100
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_txn_data >> end

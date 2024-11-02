import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

start_date = datetime(2024, 1, 11)
default_args = {
    'owner': "minhtranquang",
    "depends_on_past": False,
    "backfill": False
}

num_rows = 50
output_file = './customer_dim_large_data.csv'

# Initialize lists to store data
customer_ids = []
first_names = []
last_names = []
emails = []
phone_numbers = []
registration_dates = []

fake = Faker()

def generate_random_data(row_num):
    customer_id = f"C{row_num:05d}"
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone_number = fake.phone_number()


    # Generate opening date in milliseconds
    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 3650))
    registration_date_millis = int(random_date.timestamp() * 1000)

    return customer_id, first_name, last_name, email, phone_number, registration_date_millis

def generate_customer_dim_data():
    row_num = 1
    while row_num <= num_rows:
        customer_id, first_name, last_name, email, phone_number, registration_date_millis = generate_random_data(row_num)
        customer_ids.append(customer_id)
        first_names.append(first_name)
        last_names.append(last_name)
        emails.append(email)
        phone_numbers.append(phone_number)
        registration_dates.append(registration_date_millis)
        
        row_num += 1

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "first_name": first_names,
        "last_name": last_names,
        "email": emails,
        "phone_number": phone_numbers,
        "registration_date_millis": registration_dates,

    })

    df.to_csv(output_file, index=False)

    print(f'CSV file {output_file} with {num_rows} rows has been generated successfully!')
    
with DAG('customer_dim_generator',
         default_args=default_args,
         description='Generate large customer dimension data in a CSV file',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['schema']) as dag:
    
    start = EmptyOperator(
        task_id = 'start_task'
    )

    generate_customer_dimension_data = PythonOperator(
        task_id = 'generate_customer_dim_data',
        python_callable=generate_customer_dim_data
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_customer_dimension_data >> end
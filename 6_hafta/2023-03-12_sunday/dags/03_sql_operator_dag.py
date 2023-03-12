from datetime import datetime, timedelta
from airflow import DAG

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from python_to_db import write_to_db
start_date = datetime(2023, 3, 10)

default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('03_sql_operator_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:

    t1 = PythonOperator(task_id="download_write_db", python_callable=write_to_db)

    t2 = PostgresOperator(task_id='create_new_table', postgres_conn_id='trainvm_postgresql_conn',
                          sql='create table customers_from_airflow as select * from customers where "customers"."SpendingScore" > 50')

    t1 >> t2
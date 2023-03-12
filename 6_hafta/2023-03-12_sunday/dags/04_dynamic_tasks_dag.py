from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

start_date = datetime(2023, 3, 10)

default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# empty_dict = {}
# for i in range(5):
#     empty_dict[f'task_{i}'] = DummyOperator(task_id=f'task_{i}')
#
# print(list(empty_dict.values()))

with DAG('04_dynamic_tasks_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:

    start = DummyOperator(task_id='start')
    empty_dict = {}
    for i in range(10):
        empty_dict[f'task_{i}'] = BashOperator(task_id=f'task_{i}', bash_command='sleep 8')

    final = DummyOperator(task_id='final')


    start >> list(empty_dict.values()) >> final
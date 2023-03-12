from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

start_date = datetime(2023, 3, 10)

default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('01_bash_operator', default_args=default_args, schedule_interval='0 12 * * *', catchup=False) as dag:

    t1 = BashOperator(task_id='ls_data', bash_command='ls -l /tmp', retries=2, retry_delay=timedelta(seconds=15))

    t2 = BashOperator(task_id='download_data', bash_command='wget -O /tmp/dirty_store_transactions.csv '
                                                            'https://github.com/erkansirin78/datasets/raw/master/dirty_store_transactions.csv',
                      retries=2, retry_delay=timedelta(seconds=15))

    t3 = BashOperator(task_id='check_data', bash_command='sha256sum /tmp/dirty_store_transactions.csv',
                      retries=2, retry_delay=timedelta(seconds=15))

    t1 >> t2 >> t3
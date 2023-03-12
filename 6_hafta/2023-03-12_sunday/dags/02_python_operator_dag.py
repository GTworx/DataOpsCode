from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
from airflow.operators.python import PythonOperator
import os

start_date = datetime(2023, 3, 10)

default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

today = datetime.now().strftime('%Y-%m-%d')
current_ts = datetime.now().strftime('%Y%m%d%H%M%S')
original_file_name = "iris"
original_file_extension = "csv"
file_directory = "/opt/airflow_directory/"


def read_file(**kwargs):
    df = pd.read_csv(kwargs['file'])
    print(df.head())

def rename_file(**kwargs):
    os.rename(kwargs['source_file'], kwargs['dest_file'])


with DAG('02_python_operator_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:
    t1 = BashOperator(task_id='download_file',
                      bash_command=f"wget -O {file_directory}{original_file_name}.{original_file_extension} 'https://github.com/erkansirin78/datasets/raw/master/{original_file_name}.{original_file_extension}'",
                      retries=2, retry_delay=timedelta(seconds=15))

    t2 = BashOperator(task_id='move_file',
                       bash_command=f'mv {file_directory}{original_file_name}.{original_file_extension} {file_directory}{original_file_name}_{today}.{original_file_extension}',
                       retries=2, retry_delay=timedelta(seconds=15))

    t3 = PythonOperator(task_id='read_file', python_callable=read_file,
                        op_kwargs={'file': f'{file_directory}{original_file_name}_{today}.{original_file_extension}'})

    t4 = PythonOperator(task_id='rename_file', python_callable=rename_file,
                        op_kwargs={'source_file': f'{file_directory}{original_file_name}_{today}.{original_file_extension}',
                                   'dest_file': f'{file_directory}{original_file_name}_{current_ts}.{original_file_extension}'
                                   })

    t1 >> t2 >> t3 >> t4
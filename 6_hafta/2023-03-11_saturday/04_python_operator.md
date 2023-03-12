
- Whenever possible and especially for long-running sensors, use the reschedule mode so your sensor is not constantly occupying a worker slot. This helps avoid deadlocks in Airflow where sensors take all of the available worker slots.
- If your poke_interval is very short (less than about 5 minutes), use the poke mode. Using reschedule mode in this case can overload your scheduler.
- Define a meaningful poke_interval based on your use case. There is no need for a task to check a condition every 30 seconds (the default) if you know the total amount of wait time will be 30 minutes.

```commandline
mkdir -p /opt/airflow_directory
sudo chmod 777 /opt/airflow_directory/
```

## Create file_processing_dag.py
```commandline
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os, sys
from airflow import DAG
import pandas as pd

start_date = datetime(2022, 10, 11)

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

def rename_processed_file(**kwargs):
    os.rename(src=kwargs['raw_file'], dst=kwargs['dest_file'])
    print(kwargs['raw_file'], 'renamed to', kwargs['dest_file'])


with DAG('file_processing_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:
    t1 = BashOperator(task_id='download_file',
                      bash_command=f'wget -P {file_directory} https://github.com/erkansirin78/datasets/raw/master/{original_file_name}.{original_file_extension}',
                      retries=2, retry_delay=timedelta(seconds=15))

    t12 = BashOperator(task_id='move_file',
                       bash_command=f'mv {file_directory}{original_file_name}.{original_file_extension} {file_directory}{original_file_name}_{today}.{original_file_extension}',
                       retries=2, retry_delay=timedelta(seconds=15))

    t2 = PythonOperator(task_id='read_file', python_callable=read_file,
                        op_kwargs={'file': f'{file_directory}{original_file_name}_{today}.{original_file_extension}'})

    t3 = PythonOperator(task_id='rename_processed_file', python_callable=rename_processed_file,
                        op_kwargs={'raw_file': f'{file_directory}{original_file_name}_{today}.{original_file_extension}',
                                   'dest_file':f'{file_directory}{original_file_name}_{current_ts}_processed'})

    # t3 = BashOperator(task_id='rename_processed_file',
    #                   bash_command=f'mv {file_directory}{original_file_name}_{today}.{original_file_extension} {file_directory}{original_file_name}_{current_ts}_processed')

    t1 >> t12 >> t2 >> t3
```
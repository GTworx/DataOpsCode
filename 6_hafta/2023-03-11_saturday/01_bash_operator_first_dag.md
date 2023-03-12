## Airflow files and folders
```commandline
(venvairflow) [train@trainvm ~]$ echo $AIRFLOW_HOME
/home/train/venvairflow


(venvairflow) [train@trainvm ~]$ ls -l $AIRFLOW_HOME
total 76
-rw-rw-r--. 1 train train 39641 Oct 13 06:51 airflow.cfg
-rw-r--r--. 1 train train     5 Oct 13 06:52 airflow-webserver.pid
drwxrwxr-x. 3 train train  4096 Nov  3  2021 bin
drwxrwxr-x. 3 train train    46 Nov  3  2021 dags
drwxrwxr-x. 3 train train    31 May  9  2021 etc
drwxrwxr-x. 3 train train    18 May  9  2021 include
drwxrwxr-x. 4 train train    40 Nov  3  2021 lib
drwxrwxr-x. 3 train train    23 May  9  2021 lib64
-rw-rw-r--. 1 train train 11340 May  9  2021 LICENSE
drwxrwxr-x. 5 train train    70 Nov  3  2021 logs
-rw-rw-r--. 1 train train   202 May  9  2021 pyvenv.cfg
drwxrwxr-x. 3 train train    18 May  9  2021 share
-rw-rw-r--. 1 train train  2614 May  9  2021 unittests.cfg
-rw-rw-r--. 1 train train  4700 May  9  2021 webserver_config.py

(venvairflow) [train@trainvm ~]$ ls -l $AIRFLOW_HOME/dags
total 4
drwxr-xr-x. 2 train train   39 Nov  3  2021 __pycache__
-rw-rw-r--. 1 train train 1105 Nov  3  2021 simple_dag.py
```
## Open a pycharm project
- select airflow virtual environment

## Create a python file named my_dag.py

```commandline
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

start_date = datetime(2022, 10, 11)

default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('my_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    t0 = BashOperator(task_id='ls_data', bash_command='ls -l /tmp', retries=2, retry_delay=timedelta(seconds=15))

    t1 = BashOperator(task_id='download_data',
                      bash_command='wget -O /tmp/dirty_store_transactions.csv https://github.com/erkansirin78/datasets/raw/master/dirty_store_transactions.csv',
                      retries=2, retry_delay=timedelta(seconds=15))

    t2 = BashOperator(task_id='check_file_exists', bash_command='sha256sum /tmp/dirty_store_transactions.csv',
                      retries=2, retry_delay=timedelta(seconds=15))

    t0 >> t1 >> t2
```

## Copy my_dag.py to dags folder
` cp 01_my_dag.py ~/venvairflow/dags/ `


## List dags
- Wait 10 mins
```commandline
(venvairflow) [train@trainvm ~]$ airflow dags list


dag_id     | filepath      | owner | paused
===========+===============+=======+=======
my_dag     | my_dag.py     | train | True  
simple_dag | simple_dag.py | train | True 
```

## Airflow dag test
- ` airflow dags test my_dag 2022-10-12 `  






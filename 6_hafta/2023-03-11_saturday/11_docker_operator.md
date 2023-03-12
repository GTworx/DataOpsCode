## Install docker provider
```
source ~/venvairflow/bin/activate

pip install apache-airflow-providers-docker==2.2.0
```

## Check
```commandline
(venvairflow) [train@trainvm ~]$ pip freeze | grep docker
```
- Output
```commandline
apache-airflow-providers-docker==2.2.0
docker==6.0.1
```

## Open dag project (In VM PyCharm)
- create a module
- You must be import the DockerOperator
```
from airflow.providers.docker.operators.docker import DockerOperator
```

## Copy iris.csv
```commandline
cp ~/datasets/iris.csv /opt/airflow_directory/
```
## Start docker and airflow
- Example dag
```commandline
from airflow.decorators import task, dag
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

start_date = datetime(2023, 3, 9)
current_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


@dag(start_date=start_date, default_args=default_args, schedule_interval=timedelta(minutes=10), catchup=False)
def docker_dag():
    @task()
    def t1():
        pass

    t2 = DockerOperator(
        task_id='t2',
        image='python:3.8-slim-buster',
        mounts=[
            Mount(source="/opt/airflow_directory/", target="/tmp/datasets", type="bind"),
        ],
        command='/bin/cat /tmp/datasets/iris.csv',
        network_mode='bridge',
        mem_limit='512m',
        container_name='docker-airflow-example',
        # docker_url='unix://var/run/docker.sock', # if you run airflow in docker
        auto_remove=True,

    )
    t1() >> t2


dag = docker_dag()
```

## Copy dag file to $AIRFLOW_HOME/dags

## Run dag and watch task logs


from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator, Mount

start_date = datetime(2023, 3, 10)
hour = int(datetime.now().strftime('%H')) +1
default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


with DAG('07_docker_operator_dag', default_args=default_args, schedule_interval='@once', catchup=False) as dag:
    start = DummyOperator(task_id='start')

    docker_task = DockerOperator(task_id='docker_task',
                                 image='dataops7:1.0',
                                 #command='sleep 60',
                                 mem_limit='512m',
                                 # mounts=[
                                 #     Mount(source="/opt/airflow_directory/", target="/tmp/datasets", type="bind"),
                                 # ],
                                 #container_name='docker-airflow-example',
                                 # docker_url='unix://var/run/docker.sock', # if you run airflow in docker
                                 #auto_remove=True,
                                 )

    final_task = DummyOperator(task_id='final_task')

    start >> docker_task >> final_task
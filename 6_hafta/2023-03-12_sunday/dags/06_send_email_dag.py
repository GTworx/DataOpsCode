from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator


start_date = datetime(2023, 3, 10)
hour = int(datetime.now().strftime('%H')) +1
default_args = {
    'owner': 'train',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


with DAG('06_send_email_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:

    start = DummyOperator(task_id='start')

    email = EmailOperator(task_id='email', to='mlops@veribilimiokulu.com',
                          subject="MLOps-3 Mayıs'ta Başlıyor!!!!",
                          html_content=""" 
                          <h1>MLOps-3 Mayıs'ta Başlıyor!!!!</h1>
                          <p>From DataOps7</p>
                          
                          <h3> Erkan </h3>
                          """)

    final_task = DummyOperator(task_id='final_task')

    start >> email >> final_task
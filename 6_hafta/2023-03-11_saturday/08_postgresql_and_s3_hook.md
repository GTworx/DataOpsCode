## Start docker-compose
` docker-compose up -d `

## Create bucket and user from MinIO UI
bucket: dataops
user: airflow

## Define airflow variables from UI
```commandline
endpoint_url
aws_access_key_id
aws_secret_access_key
```

## DAG file
```python
import logging, boto3, botocore
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from botocore.config import Config

today = datetime.now().strftime('%Y%m%d')
this_hour = int(datetime.now().strftime('%H')) + 4
endpoint_url = Variable.get("endpoint_url")
aws_access_key_id = Variable.get("aws_access_key_id")
aws_secret_access_key = Variable.get("aws_secret_access_key")

default_args = {
    'owner': 'train',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 3, 10)
}


def get_s3_client():
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      config=Config(signature_version='s3v4'))
    return s3


def load_df_from_s3(bucket, key, sep=",", index_col=None, usecols=None):
    ''' Read a csv from a s3 bucket & load into pandas dataframe'''
    s3 = get_s3_client()
    try:
        logging.info(f"Loading {bucket, key}")
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(obj['Body'], sep=sep, index_col=index_col, usecols=usecols, low_memory=False)
    except botocore.exceptions.ClientError as err:
        status = err.response["ResponseMetadata"]["HTTPStatusCode"]
        errcode = err.response["Error"]["Code"]
        if status == 404:
            logging.warning("Missing object, %s", errcode)
        elif status == 403:
            logging.error("Access denied, %s", errcode)
        else:
            logging.exception("Error in request, %s", errcode)


def save_file_to_s3(**kwargs):
    ''' Store file to s3'''
    s3 = get_s3_client()
    try:
        s3.upload_file(kwargs['source_data_path'], kwargs['bucket'], kwargs['key'])
        logging.info(f"{kwargs['key']} saved to s3 bucket {kwargs['bucket']}")
    except Exception as e:
        raise logging.exception(e)


def data_transfer(**kwargs):
    df2 = load_df_from_s3(bucket=kwargs['bucket'], key=kwargs['key'])

    postgres_hook = PostgresHook(postgres_conn_id='trainvm_postgresql_con', schema='traindb')
    uri = postgres_hook.get_uri()
    engine = create_engine(uri)
    Base = declarative_base()

    # Create database table
    class Customer(Base):
        __tablename__ = "customers"

        CustomerID = Column(Integer, primary_key=True)
        Gender = Column(String)
        Age = Column(Integer)
        AnnualIncome = Column(Float)
        SpendingScore = Column(Integer)

    Base.metadata.create_all(bind=engine)

    df2.to_sql('customers', engine, if_exists='replace', index=False)

    print("Data transferred successfully!")


with DAG('hooks_demo_v4', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    t1 = PythonOperator(task_id='upload_data_to_s3', python_callable=save_file_to_s3,
                        op_kwargs={
                            'source_data_path': '/home/train/datasets/Mall_Customers.csv',
                            'bucket': 'dataops',
                            'key': 'Mall_Customers.csv'
                        })

    t2 = PostgresOperator(task_id='truncate_table', postgres_conn_id='trainvm_postgresql_con',
                          sql='DROP TABLE IF EXISTS customers')

    t3 = PythonOperator(task_id='transfer_data_s3_to_postgresql',
                        python_callable=data_transfer,
                        op_kwargs={
                            'bucket': 'dataops',
                            'key': 'Mall_Customers.csv'
                        })

    t1 >> t2 >> t3
```
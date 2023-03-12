```commandline
import boto3, logging, botocore
from botocore.config import Config
import pandas as pd


def get_s3_client():
    s3 = boto3.client('s3',
                      endpoint_url='http://localhost:9000',
                      aws_access_key_id='dataops',
                      aws_secret_access_key='Ankara06',
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


save_file_to_s3(source_data_path='/home/train/datasets/Mall_Customers.csv', bucket='dataops', key='Mall_Customers.csv')

df = load_df_from_s3(bucket='dataops', key='Mall_Customers.csv')

print(df.head())

```
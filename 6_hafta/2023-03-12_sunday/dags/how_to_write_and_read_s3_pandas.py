import pandas as pd
import boto3, logging, io

df = pd.read_csv("/home/train/datasets/Mall_Customers.csv")

print(df.head())

# pandas df to s3
s3_client = boto3.client('s3',
                         aws_access_key_id='airflow',
                      aws_secret_access_key='Ankara06',
                         endpoint_url='http://localhost:9000')

s3_res = boto3.resource('s3',
                         aws_access_key_id='airflow',
                      aws_secret_access_key='Ankara06',
                         endpoint_url='http://localhost:9000')

# def save_file_to_s3(s3_client, df, bucket, key):
#     ''' Store file to s3'''
#     csv_buffer = io.StringIO()
#     try:
#         df.to_csv(csv_buffer)
#         #s3_client.upload_file(source_data_path, bucket, key)
#         s3_client.put_object(Body=csv_buffer, Bucket=bucket, Key=key)
#     except Exception as e:
#         raise logging.exception(e)

def save_df_to_s3(s3_res, df, bucket, key):
    ''' Store df as a buffer, then save buffer to s3'''
    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        # s3_resource = boto3.resource('s3')
        s3_res.Object(bucket, key).put(Body=csv_buffer.getvalue())
        logging.info(f'{key} saved to s3 bucket {bucket}')
    except Exception as e:
        raise logging.exception(e)

def load_df_from_s3(bucket, key, s3_client, index_col=None, usecols=None, sep=","):
    ''' Read a csv from a s3 bucket & load into pandas dataframe'''
    try:
        logging.info(f"Loading {bucket, key}")
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(obj['Body'], index_col=index_col, usecols=usecols,
                           low_memory=False, sep=sep)
    except Exception as e:
        raise logging.exception(e)

#save_file_to_s3(s3_client, "/home/train/datasets/Mall_Customers.csv", "dataops", "dataops7/Mall_Customers.csv")

save_df_to_s3(s3_res, df, "dataops", "dataops7/Mall_Customers.csv")

df_from_s3 = load_df_from_s3("dataops", "dataops7/Mall_Customers.csv", s3_client)
print(df_from_s3.head(10))
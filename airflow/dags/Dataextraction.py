import requests
import os
import pandas as pd
import zipfile
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set all credentials and variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('SOURCE_BUCKET')

s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
s3_resource = boto3.resource('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)


# Create a folder for the data if it doesn't exist
subfolder_path = '/opt/airflow/working_dir/'

s3_path = 'CDC_files/'


def load_files(ti):

    # Download the ZIP file from the URL
    url = 'https://www.cdc.gov/brfss/annual_data/2021/files/LLCP2021XPT.zip'
    response = requests.get(url)

    filename = 'LLCP2021'
    # Save the ZIP file to disk

    filename_zip = f'{filename}XPT.zip'
    zip_file_path = os.path.join(subfolder_path, filename_zip)
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)
    print(f'{filename_zip} saved on {zip_file_path}')

    filename_xpt = f'{filename}.XPT '
    xpt_file_path = os.path.join(subfolder_path, filename_xpt)

    # Extract the ZIP file
    print('Extracting zipped file')
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(subfolder_path)
    print(f'Extract ZIP file --> {filename_zip}')

    # upload files to s3
    s3_zip_path = f'{s3_path}{filename_zip}'
    s3_resource.Object(bucket, s3_zip_path).put(Body=open(zip_file_path, 'rb'))
    print(f'Uploaded to S3: {filename_zip} --> {s3_zip_path}')

    s3_xpt_path = f'{s3_path}{filename_xpt}'
    s3_resource.Object(bucket, s3_xpt_path).put(Body=open(xpt_file_path, 'rb'))
    print(f'Uploaded to S3: {filename_xpt} --> {s3_xpt_path}')

    ti.xcom_push(key="xpt_file", value=filename_xpt)
    ti.xcom_push(key="filename", value=filename)
    ti.xcom_push(key="xpt_file_path", value=xpt_file_path)
    ti.xcom_push(key="subfolder_path", value=subfolder_path)
    ti.xcom_push(key="s3_path", value=s3_path)


def upload_to_s3(ti):
    filename_csv = ti.xcom_pull(task_ids="data_cleanup", key="filename_csv")

    # Convert the dataframe to CSV and save to S3
    csv_file_path = os.path.join(subfolder_path, filename_csv)
    s3_csv_path = f'{s3_path}{filename_csv}'

    s3_resource.Object(bucket, s3_csv_path).put(Body=open(csv_file_path, 'rb'))
    print(f'Uploaded to S3: {filename_csv} --> {s3_csv_path}')


def clean_dir():
    if not os.listdir(subfolder_path):
        print(f"{subfolder_path} is empty")
    else:
        # Remove all files from the directory
        for f in os.listdir(subfolder_path):
            os.remove(os.path.join(subfolder_path, f))
        print(f"Files removed from {subfolder_path} ...")

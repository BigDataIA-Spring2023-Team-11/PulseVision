from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from Dataextraction import load_files, upload_to_s3, clean_dir
from data_cleanup import data_cleanup


# Define DAG arguments
default_args = {
    'owner': 'Team11',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'retries': 5
}

# Define DAG
etl_Dag = DAG('ETL_Dag',
              default_args=default_args
              )

task_directory_cleanup = PythonOperator(
    task_id='directory_cleanup',
    python_callable=clean_dir,
    dag=etl_Dag
)

task_download_files = PythonOperator(
    task_id='load_files',
    python_callable=load_files,
    dag=etl_Dag
)

task_data_cleanup = PythonOperator(
    task_id='data_cleanup',
    python_callable=data_cleanup,
    dag=etl_Dag
)

task_upload_to_s3 = PythonOperator(
    task_id='convert_to_csv',
    python_callable=upload_to_s3,
    dag=etl_Dag
)

# Set up dependencies
task_directory_cleanup >> task_download_files >> task_data_cleanup >> task_upload_to_s3

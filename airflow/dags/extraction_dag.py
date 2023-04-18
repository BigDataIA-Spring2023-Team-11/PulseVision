from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from Dataextraction import load_files, convert_to_csv

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

download_files = PythonOperator(
    task_id='load_files',
    python_callable=load_files,
    dag=etl_Dag
)

convert_files = PythonOperator(
    task_id='convert_to_csv',
    python_callable=convert_to_csv,
    dag=etl_Dag
)

# Set up dependencies
download_files >> convert_files

import requests
import os
import pandas as pd
import zipfile

# Download the ZIP file from the URL
url = 'https://www.cdc.gov/brfss/annual_data/2021/files/LLCP2021XPT.zip'
response = requests.get(url)

# Create a folder for the data if it doesn't exist
# subfolder_path = 'airflow/working_dir/'
subfolder_path = '/opt/airflow/working_dir/'


def load_files():

    # Save the ZIP file to disk

    zip_file_path = os.path.join(subfolder_path, 'LLCP2021XPT.zip')
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)
    print(f'LLCP2021XPT.zip saved on {zip_file_path}')

    # Extract the ZIP file

    print('Extracting zipped file')
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(subfolder_path)
    print(f'Extract ZIP file --> LLCP2021XPT.zip')


def convert_to_csv():

    # Read the XPT file using pandas
    print(f'Loading file to dataframe')
    xpt_file_path = os.path.join(subfolder_path, 'LLCP2021.XPT ')
    df = pd.read_sas(xpt_file_path, format='xport')
    print(f'XPT file path --> {xpt_file_path}')

    # Save the CSV file to disk

    csv_file_path = os.path.join(subfolder_path, 'LLCP2021.csv')
    print(f'Loading dataframe to csv file --> {csv_file_path}')
    df.to_csv(csv_file_path, index=False)
    print(f'CSV loaded --> {csv_file_path}')




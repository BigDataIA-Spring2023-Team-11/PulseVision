import requests
import os
import pandas as pd
import zipfile

# Download the ZIP file from the URL
url = 'https://www.cdc.gov/brfss/annual_data/2021/files/LLCP2021XPT.zip'
response = requests.get(url)

# Create a folder for the data if it doesn't exist
subfolder_path = 'data'
os.makedirs(subfolder_path, exist_ok=True)

# Save the ZIP file to disk
zip_file_path = os.path.join(subfolder_path, 'LLCP2021XPT.zip')
with open(zip_file_path, 'wb') as f:
    f.write(response.content)

# Extract the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(subfolder_path)

# Read the XPT file using pandas
xpt_file_path = os.path.join(subfolder_path, 'LLCP2021.XPT ')
df = pd.read_sas(xpt_file_path, format='xport')

# Save the CSV file to disk
csv_file_path = os.path.join(subfolder_path, 'LLCP2021.csv')
df.to_csv(csv_file_path, index=False)

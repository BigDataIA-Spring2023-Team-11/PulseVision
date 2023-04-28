# PulseVision

### Links
<ul>
<li>💻 <a href="#">Streamlit</a> </li>
<li>⏰ <a href="http://23.21.117.161:8080/home">Airflow</a> </li>
<li>📖 <a href="https://codelabs-preview.appspot.com/?file_id=14YRHzjXPtdIUmMqmMg9HLaYiHnN5_9LNUB0Zvr-s294#0">Codelab </a> </li>
<li> ⏯️  <a href="#">Demo </a> </li>
</ul>



### Table of Content

1️⃣ [Objective](#objective) <br>
2️⃣ [Architecture Diagram](#architecture-diagram) <br>
3️⃣ [Components](#components) <br>
4️⃣ [Steps to run the application](#steps-to-run-the-application) <br>
5️⃣ [Attestation](#attestation) <br>

___


## Objective
The objective of this application is to provide users with tools and information to help them monitor and manage their heart health. The application achieves this by offering features such as a:
1. Heart-disease risk prediction tool
2. Health analytics to track progress over time
3. BMI calculator to help users understand their body mass index

The ultimate goal of the application is likely to empower users to make informed decisions about their health and take steps to improve their overall well-being.

## Architecture Diagram
![image](https://github.com/UKEYBHAKTI002922939/PulseVision-1/blob/main/architecture_Diagram/cloud_architecture.png)


## Components
This application utilises trusted dataset set sources from CDC, and cleans and models it to provide predictions.
Detailed EDA and modeling can be viewed here - [Heart Disease Feature Engineering and Modelling](modeling/Heart_Disease_Feature_Engineering_and_Modeling.ipynb)

The application contains several components:
1. **Streamlit** - 
2. **Airflow** - This data pipeline orchestrator is used to automated and schedule the data extraction, data cleansing, data ingestion, and data storage process.   
3. **FastAPI** - 
4. **AWS** - Various AWS services are being utilized in this application:
    * S3 
    * Cloudwatch
    * EC2
5. **Pytest** - 


## Steps to run the application
### AIRFLOW

1. Clone the airflow branch using the following code on terminal - 
````
git clone --branch airflow https://github.com/BigDataIA-Spring2023-Team-11/PulseVision.git
````
2. Move to the project directory and run the following command in terminal to create a .env file
````
nano .env
````
3. Add the following environment variables with values:
```
AIRFLOW_UID=501
AIRFLOW_PROJ_DIR=./airflow
ACCESS_KEY=
SECRET_KEY=
SOURCE_BUCKET=
API_KEY=
KMP_DUPLICATE_LIB_OK=TRUE
```
4. In docker-compose.yaml, update airflow login credentials on line 264 and 265
```commandline
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-}
```
5. Save file while exiting the editor -> *control* + *x*
6. Install requirements using command - 
```commandline
pip install -r requirements.txt
```
7. Ensure docker is running in background. Run following commands - 
```commandline
docker-compose build
docker compose up airflow-init
docker compose up
```
8. Once the localhost URL is shared, go to : https://localhost:8080/
9. Login using credentials set up step 4
10. Review DAG: ETL_dag
11. Go to dags to trigger run, view logs, graphs etc.


### Streamlit
1. Open terminal
2. Change to the location where you want to copy the repository
```commandline
git clone https://github.com/BigDataIA-Spring2023-Team-11/Pulsevision.git
```
3. Create .env file
```commandline
AWS_ACCESS_KEY =
AWS_SECRET_KEY =
LOGS_ACCESS_KEY =
LOGS_SECRET_KEY =
```
4. Run the app using the command
```commandline
streamlit run main.py
```

## Attestation
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT
AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
Contribution:
<ul>
<li>Aakash: 20%</li>
<li>Bhakti: 20%</li>
<li>Bhargavi: 40%</li>
<li>Charu: 20%</li>
</ul>



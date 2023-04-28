import shap
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import time
import openai
from dotenv import load_dotenv
import boto3
load_dotenv()
s3_logs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('SECRET_KEY')
                        )
def global_interpretibility_plot():
    shap.initjs()
    # Lets load the model from pickle file
    filename = "model/rf_model_to_predict_heartDisease"
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    # Load the test dataset
    df = pd.read_csv("data/test_dataset.csv")
    df = df.drop(df.columns[0], axis=1)
    sdf = df.sample(50)
    # Create object that can calculate shap values
    explainer = shap.TreeExplainer(model, df)

    # calculate shap values. This is what we will plot.
    # Calculate shap_values for all of val_X rather than a single row, to have more data for plot.
    shap_values = explainer.shap_values(df)
    # shap_values = explainer(df.head(1))
    # Summary Plot for CLASS = 1 (Heart Disease = YES)
    return shap.summary_plot(shap_values[1], df, show=True)


"""
"""
def get_answers_to_ques(ques):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print(openai.api_key,ques)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ:\nA: Unknown\n\nQ: {ques}\n",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    print(response)

    return response.choices[0].text.strip()
    # return ""
"""

"""
def interpret_predictions_runtime(df):
    shap.initjs()
    # Lets load the model from pickle file
    filename = "model"
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    df_test = pd.read_csv("test_dataset.csv")
    df_test = df_test.drop(df_test.columns[0], axis=1)
    # Create object that can calculate shap values
    explainer = shap.TreeExplainer(model, df_test)
    shap_values = explainer.shap_values(df)
    return shap.plots.force(explainer.expected_value[1], shap_values[1], df)
    # shap.summary_plot(shap_values[1], df.iloc[[3]])

"""
writing logs to cloudwatch
"""
def write_logs_to_cloudwatch(message: str, log_stream):
    s3_logs.put_log_events(
        logGroupName = "pulse-vision-logs",
        logStreamName = log_stream,
        logEvents = [
            {
                'timestamp' : int(time.time() * 1e3),
                'message' : message
            }
        ]
    )

def read_register_user_logs():

    log_group_name = "pulse-vision-logs"
    log_stream_name = 'registration-logs'
    # Set start time to the beginning of the log stream

    # Initialize an empty list to store log events
    # Call get_log_events to retrieve all log events from the log stream
    response = s3_logs.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
    )

    # Extract the timestamp and message from each log event
    timestamps = []
    messages = []
    for event in response['events']:
        timestamps.append(event['timestamp'])
        messages.append(event['message'])

    # Split each message into its components and store them in a DataFrame
    df = pd.DataFrame([m.split('###') for m in messages], columns=['name', 'email', 'password'])
    df['timestamp'] = pd.to_datetime(timestamps, unit='ms')
    return df

if __name__ == "__main__":
    get_answers_to_ques("How to improve general health and reduce the risk of heart disease")
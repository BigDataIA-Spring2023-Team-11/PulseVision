import shap
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import openai
from dotenv import load_dotenv

load_dotenv()

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
"""

"""
def interpret_predictions_runtime(df):
    shap.initjs()
    # Lets load the model from pickle file
    filename = "rf_model_to_predict_heartDisease"
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    df_test = pd.read_csv("test_dataset.csv")
    df_test = df_test.drop(df_test.columns[0], axis=1)
    # Create object that can calculate shap values
    explainer = shap.TreeExplainer(model, df_test)
    shap_values = explainer.shap_values(df)
    return shap.plots.force(explainer.expected_value[1], shap_values[1], df)
    # shap.summary_plot(shap_values[1], df.iloc[[3]])
if __name__ == "__main__":
    get_answers_to_ques("How to improve general health and reduce the risk of heart disease")
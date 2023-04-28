import os
import json
import pickle
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException

path = os.path.dirname(__file__)
# Model Path
with open('config.json', 'r') as f:
    config = json.load(f)

model_path = config['model']['path']
MODEL_PATH = path.replace(".","")+model_path

app = FastAPI(title="Heart Disease Prediction")


class UserInput(BaseModel):
    AgeCategory: int
    Stroke: int
    Diabetic_Yes: int
    KidneyDisease: int
    Smoking: int
    SkinCancer: int
    Is_Male: int
    BMI: int
    Asthma: int
    Race_White: int
    AlcoholDrinking: int
    GenHealth: int

# load model
model = pickle.load(open(MODEL_PATH, "rb"))
print(MODEL_PATH,"model____path")


@app.post('/get_predict', status_code=status.HTTP_200_OK)
async def predict(userinput: UserInput) -> dict:
    try:
        df = pd.DataFrame([json.loads(userinput.json())])
        prob = model.predict_proba(df)
        prediction = model.predict(df)

        response_json = {}

        response_json['prediction_probability'] = (prob[0][1] * 100 ).round(0)
        response_json['prediction'] = int(prediction[0])
        return response_json
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error while predicting!")

# @app.post("/get_predictions")
# def get_predictions(json_string):
#     # convert the JSON string back to a DataFrame
#     df = pd.read_json(json_string, orient='records')
#     # df =pd.read_csv("streamlit/data/df.csv")
#     log_model = pickle.load(open(MODEL_PATH, "rb"))
#     prediction = log_model.predict(df)
#     prediction_prob = log_model.predict_proba(df)
#     pred = (100*prediction_prob[0][1]).round(0)
#     return {"prediction":prediction,"percentage": pred}



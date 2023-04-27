import os
import json
import pickle
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException

path = os.path.dirname(__file__)
# Model Path
MODEL_PATH = path.replace(".","")+"model/rf_model_to_predict_heartDisease"

app = FastAPI()

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
# app = FastAPI(title="Health App")


@app.post('/predict', status_code=status.HTTP_200_OK)
async def predict(userinput: UserInput) -> dict:
    try:
        # read the input dict into json and then into df
        df = pd.DataFrame([json.loads(userinput.json())])
        # predict
        prediction_prob = model.predict_proba(df)
        response = {}
        # first prediction value rounded off
        response['value_0'] = (prediction_prob[0][0] * 100 ).round(0)
        # second prediction value rounded off
        response['value_1'] = (prediction_prob[0][1] * 100 ).round(0)
        return response
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot Predict, Try again")

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


